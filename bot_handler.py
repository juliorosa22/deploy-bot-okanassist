import os
import asyncio
import aiohttp
import tempfile
from aiohttp import web 
#import pytz  # <-- 1. Import pytz
from typing import Optional, Dict, Any
from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    ContextTypes, ConversationHandler
)
from telegram.helpers import escape_markdown  # <-- 1. Import the escape helper
from dotenv import load_dotenv
from messages import get_message, MESSAGES
# Load environment variables first
load_dotenv()

# Conversation states for registration
REGISTER_EMAIL, REGISTER_NAME, REGISTER_LASTNAME, REGISTER_TIMEZONE, REGISTER_CONFIRM = range(5)  # <-- 2. Add new state
SUPPORT_MESSAGE = range(5, 6)

class AgnoTelegramBot:
    """Telegram bot with session-based authentication"""
    
    def __init__(self, api_url: str = None):
        # Load environment variables
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.api_url = api_url or os.getenv('API_SERVICE_URL', 'http://localhost:8000')
        self.support_chat_id = os.getenv('SUPPORT_CHAT_ID')  # <-- 2. Load the support chat ID
        self.app_url = os.getenv('APP_URL')
        
        # Validate required environment variables
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        print(f"🔗 Initializing bot with token: {self.token[:20]}...")
        print(f"🔗 API service URL: {self.api_url}")
        
        self.app = None
        self.registration_data: Dict[str, Dict[str, Any]] = {}

    def setup(self):
        """Setup the Telegram bot"""
        self.app = Application.builder().token(self.token).build()
        
        # Registration conversation handler
        registration_handler = ConversationHandler(
            entry_points=[CommandHandler("register", self.register_start)],
            states={
                REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.register_email)],
                # --- 1. Handle /skip command explicitly ---
                REGISTER_NAME: [
                    CommandHandler("skip", self.register_name),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.register_name)
                ],
                REGISTER_LASTNAME: [
                    CommandHandler("skip", self.register_lastname),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.register_lastname)
                ],
                REGISTER_TIMEZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.register_timezone)],
                REGISTER_CONFIRM: [
                    CommandHandler("confirm", self.register_confirm),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.register_invalid_confirm_input)
                ],
            },
            fallbacks=[CommandHandler("cancel", self.register_cancel)],
        )
        self.app.add_handler(registration_handler)
        
        # --- 1. Define and add the support conversation handler ---
        support_handler = ConversationHandler(
            entry_points=[CommandHandler("support", self.support_start)],
            states={
                SUPPORT_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.support_message)],
            },
            fallbacks=[CommandHandler("cancel", self.support_cancel)],
        )
        self.app.add_handler(support_handler)

        self.app.add_handler(CommandHandler("upgrade", self.upgrade_command))
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("balance", self.balance_command))
        self.app.add_handler(CommandHandler("reminders", self.reminders_command))
        self.app.add_handler(CommandHandler("profile", self.profile_command))
        
        # Photo and document handlers
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_receipt_photo))
        self.app.add_handler(MessageHandler(filters.Document.PDF, self.handle_pdf_statement))
        # Audio handler
        self.app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, self.handle_audio_message))

        # Message handler for natural language processing
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        return self.app
    
   
    # Registration conversation handlers
    async def register_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start registration process"""
        user = update.effective_user
        telegram_id = str(user.id)
        
        # Initialize registration data
        self.registration_data[telegram_id] = {
            "telegram_id": telegram_id,
            "first_name": user.first_name,
            "language_code": user.language_code or "en"
        }
        
        await update.message.reply_text(
            get_message("register_start", user.language_code),
            parse_mode='Markdown'
        )
        
        return REGISTER_EMAIL
    
    async def register_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle email input"""
        email = update.message.text.strip()
        telegram_id = str(update.effective_user.id)
        
        # Basic email validation
        if "@" not in email or "." not in email:
            await update.message.reply_text(
                get_message("validate_email", update.effective_user.language_code)
            )
            return REGISTER_EMAIL
        
        self.registration_data[telegram_id]["email"] = email
        
        await update.message.reply_text(
            get_message("register_first_name", update.effective_user.language_code, email=escape_markdown(email, version=2), first_name=escape_markdown(update.effective_user.first_name, version=2)),
        )
        
        return REGISTER_NAME
    
    async def register_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle first name input"""
        telegram_id = str(update.effective_user.id)
        
        # --- 2. Check if the input is NOT a command before updating ---
        if not update.message.text.startswith('/'):
            first_name = update.message.text.strip()
            self.registration_data[telegram_id]["first_name"] = first_name
        
        await update.message.reply_text(
           get_message("register_last_name", update.effective_user.language_code)
        )
        
        return REGISTER_LASTNAME
    
    async def register_lastname(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle last name input"""
        telegram_id = str(update.effective_user.id)
        
        # --- 2. Check if the input is NOT a command before updating ---
        if not update.message.text.startswith('/'):
            last_name = update.message.text.strip()
            self.registration_data[telegram_id]["last_name"] = last_name
        
        # --- 1. Update the prompt to encourage natural language ---
        await update.message.reply_text(
           get_message("register_timezone", update.effective_user.language_code),
            parse_mode='Markdown'
        )
        
        return REGISTER_TIMEZONE

    # --- 2. Simplify the timezone handler ---
    async def register_timezone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle timezone input by capturing the raw text."""
        timezone_input = update.message.text.strip()
        telegram_id = str(update.effective_user.id)

        # Store the raw text. The API will process it.
        self.registration_data[telegram_id]["timezone"] = timezone_input
        
        # Immediately proceed to the confirmation step
        return await self.show_registration_confirmation(update, context)

    async def show_registration_confirmation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Helper function to display the final confirmation message."""
        telegram_id = str(update.effective_user.id)
        data = self.registration_data[telegram_id]
        
        confirmation_text = (
            get_message("register_confirmation", update.effective_user.language_code, email=escape_markdown(data["email"], version=2), first_name=escape_markdown(data["first_name"], version=2))
        )
        
        if data.get("last_name"):
            confirmation_text += f" {data['last_name']}"
        
        # --- 2. Update the prompt to use commands ---
        confirmation_text += (
           get_message("register_confirmation_with_timezone", update.effective_user.language_code, language=escape_markdown(data["language_code"], version=2), timezone=escape_markdown(data["timezone"], version=2))
        )
        
        await update.message.reply_text(confirmation_text, parse_mode='Markdown')
        return REGISTER_CONFIRM

    # --- 3. Refactor the confirmation logic ---
    async def register_confirm(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /confirm command to finalize registration."""
        telegram_id = str(update.effective_user.id)
        
        # Submit registration to API
        try:
            data = self.registration_data[telegram_id]
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/okanassist/v1/register",
                    json={
                        "telegram_id": data["telegram_id"],
                        "email": data["email"],
                        "name": data["first_name"]+" "+data.get("last_name",""),
                        "language_code": data["language_code"],
                        "timezone": data["timezone"],
                        "currency": "USD"
                    }
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get("success"):
                        await update.message.reply_text(
                            result["message"],
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text(
                            f"❌ Registration failed: {result.get('message', 'Unknown error')}"
                        )
            
            # Clean up registration data
            del self.registration_data[telegram_id]
            
        except Exception as e:
            print(f"❌ Error during registration: {e}")
            await update.message.reply_text(
                "❌ Registration failed due to a technical error. Please try again later."
            )
        
        return ConversationHandler.END

    async def register_invalid_confirm_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles any input that is not /confirm or /cancel at the final step."""
        await update.message.reply_text(
            "Please use /confirm to create your account or /cancel to stop."
        )
        return REGISTER_CONFIRM
    
    async def register_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel registration"""
        telegram_id = str(update.effective_user.id)
        
        if telegram_id in self.registration_data:
            del self.registration_data[telegram_id]
        
        await update.message.reply_text(
            "❌ Registration cancelled.\n"
            "Type /register to start again anytime.",
            parse_mode='Markdown'
        )
        
        return ConversationHandler.END
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command by calling the API's handle_start directly"""
        user = update.effective_user
        args = context.args
        print(f"context received:{args}")
        print(f"👤 /start command from {user.first_name} ({user.id})")
        
        # Handle payment status or Supabase ID
        if args and len(args) > 0:

            if args[0]=="payment_success":
                await update.message.reply_text(
                    get_message("payment_success", update.effective_user.language_code),
                    parse_mode='Markdown'
                )
                return
            elif args[0]=="payment_cancelled":
                await update.message.reply_text(
                    get_message("payment_failure", update.effective_user.language_code),
                    parse_mode='Markdown'
                )
                return
            elif args[0]=="portal_return":
                await update.message.reply_text(
                    get_message("portal_return", update.effective_user.language_code),
                    parse_mode='Markdown'
                )
                return
            else:
                supabase_user_id = args[0]               
                print(f"📱 Redirect from mobile app with data: {supabase_user_id}")
                # Optionally, you can call your API with the Supabase ID here if needed
        
        # Always call the API's /okanassist/v1/start endpoint - let the API handle authentication and responses
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/okanassist/v1/start",
                    json={
                        "telegram_id": str(user.id),
                        "user_data": user.to_dict(),
                        "args": args,
                        "language_code": user.language_code # <-- Pass language
                    }
                ) as response:
                    result = await response.json()
                    await update.message.reply_text(result["message"], parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            print(f"❌ Error in start command: {e}")
            await update.message.reply_text(get_message("generic_error", update.effective_user.language_code))
        
        # --- 3. REMOVE the return value ---
        # return ConversationHandler.END

    async def upgrade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /upgrade command to get a premium payment link."""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"🚀 /upgrade command from {user.first_name}")
        #await update.message.reply_text(get_message("generic_maintenance", update.effective_user.language_code))
        #await update.message.reply_text(get_message("upgrade_link_generation", update.effective_user.language_code))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/okanassist/v1/upgrade",
                    json={"telegram_id": telegram_id}
                ) as response:
                    result = await response.json()
                    message = result.get("message", "An error occurred.")

                    if response.status == 200 and result.get("success"):
                        # Success! The message from the API will contain the payment link.
                        await update.message.reply_text(
                            message,
                            parse_mode='Markdown',
                            disable_web_page_preview=False # Ensure the link preview shows
                        )
                    elif response.status == 401:
                        await update.message.reply_text(
                            get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to upgrade!\nType /register to create your account.",
                            parse_mode='Markdown'
                        )
                    else:
                        # Handle other errors, like user is already premium
                        await update.message.reply_text(message)

        except Exception as e:
            print(f"❌ Error in upgrade command: {e}")
            await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))



    # --- 4. Add the support conversation methods ---

    async def support_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starts the support conversation."""
        await update.message.reply_text(
            get_message("support_prompt", update.effective_user.language_code) ,
            parse_mode='Markdown'
        )
        return SUPPORT_MESSAGE

    async def support_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Forwards the user's support message."""
        user = update.effective_user
        message_text = update.message.text

        if not self.support_chat_id:
            print("⚠️ SUPPORT_CHAT_ID is not set. Cannot forward message.")
            await update.message.reply_text("❌ We're sorry, the support system is currently unavailable. Please try again later.")
            return ConversationHandler.END
        print("support id:", self.support_chat_id)
        # Format the message with user details
        forward_message = (
            f"**New Support Request**\n\n"
            f"**From:** {user.first_name} {user.last_name or ''}\n"
            f"**User ID:** `{user.id}`\n"
            f"**Username:** @{user.username or 'N/A'}\n\n"
            f"--- Message ---\n"
            f"{message_text}"
        )
        print(forward_message)
        try:
            # Send the formatted message to your private support channel
            await self.app.bot.send_message(
                chat_id=self.support_chat_id,
                text=forward_message,
                parse_mode='Markdown'
            )
            await update.message.reply_text(
                get_message("support_message", update.effective_user.language_code),
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"❌ Failed to forward support message: {e}")
            await update.message.reply_text(get_message("generic_error", update.effective_user.language_code))

        return ConversationHandler.END

    async def support_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels the support conversation."""
        await update.message.reply_text("Support request cancelled.")
        return ConversationHandler.END
   
   
   # --- 5. User Interaction Handlers ---
    async def handle_audio_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process audio messages with authentication"""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"🎤 Audio message from {user.first_name}")

        try:
            audio = update.message.voice or update.message.audio
            if not audio:
                await update.message.reply_text("❌ No audio found in your message.")
                return

            file = await audio.get_file()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
                await file.download_to_drive(temp_file.name)

                async with aiohttp.ClientSession() as session:
                    with open(temp_file.name, 'rb') as f:
                        data = aiohttp.FormData()
                        data.add_field('telegram_id', telegram_id)
                        data.add_field('file', f, filename='audio.ogg', content_type='audio/ogg')

                        async with session.post(
                            f"{self.api_url}/okanassist/v1/process-audio",
                            data=data
                        ) as response:
                            if response.status == 200:
                                result = await response.json()
                                await update.message.reply_text(result.get("message", "✅ Audio processed!"), parse_mode='Markdown')
                            elif response.status == 401:
                                await update.message.reply_text(
                                    get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to process audio!\nType /register to create your account.",
                                    parse_mode='Markdown'
                                )
                            else:
                                await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))

                os.unlink(temp_file.name)

        except Exception as e:
            print(f"❌ Error processing audio: {e}")
            await update.message.reply_text(get_message("generic_error", update.effective_user.language_code))    
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages with authentication check"""
        user = update.effective_user
        message = update.message.text
        telegram_id = str(user.id)
        
        print(f"📱 Message from {user.first_name} ({user.id}): {message}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/okanassist/v1/route-message",
                    json={
                        "telegram_id": telegram_id,
                        "message": message,
                        "user_data": user.to_dict(),
                        "language_code": user.language_code # <-- Pass language
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        await update.message.reply_text(result["message"], parse_mode='Markdown')
                    elif response.status == 401:
                        # ✅ FIX: Handle 401 properly
                        error_data = await response.json()
                        error_message = error_data.get('detail', 'Authentication required')
                        await update.message.reply_text(
                            get_message("user_not_found", update.effective_user.language_code) + f"\n\n⚠️ {error_message}",
                            parse_mode='Markdown'
                        )
                    else:
                        print(f"❌ Error processing message: {response.status}")
                        await update.message.reply_text(
                            get_message("generic_downtime", update.effective_user.language_code)
                        )
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            await update.message.reply_text(
                get_message("generic_downtime", update.effective_user.language_code)
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user = update.effective_user
        print(f"ℹ️ /help command from {user.first_name}")
        
        try:
            # Get the help message directly from messages.py using the user's language
            help_text = get_message("help_message", user.language_code)
            await update.message.reply_text(help_text, parse_mode='Markdown')
            
        except Exception as e:
            print(f"❌ Error in help command: {e}")
            await update.message.reply_text(get_message("generic_error", user.language_code))

    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command with authentication"""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"💰 /balance command from {user.first_name}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/okanassist/v1/get-transaction-summary",
                    json={"telegram_id": telegram_id, "days": 30}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        await update.message.reply_text(result["message"], parse_mode='Markdown')
                    elif response.status == 401:
                        await update.message.reply_text(
                            get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to view your balance!\nType /register to create your account.",
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text(
                            get_message("generic_downtime", update.effective_user.language_code)
                        )
        except Exception as e:
            print(f"❌ Error in balance command: {e}")
            await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))

    async def reminders_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reminders command with authentication"""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"⏰ /reminders command from {user.first_name}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/okanassist/v1/get-reminders",
                    params={"telegram_id": telegram_id, "limit": 10}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        await update.message.reply_text(result["message"], parse_mode='Markdown')
                    elif response.status == 401:
                        await update.message.reply_text(
                            get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to view your reminders!\nType /register to create your account.",
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text(
                            get_message("generic_downtime", update.effective_user.language_code)
                        )
        except Exception as e:
            print(f"❌ Error in reminders command: {e}")
            await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))

    async def handle_receipt_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process receipt photos with authentication"""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"📸 Receipt photo from {user.first_name}")
        
        try:
            # Download photo
            photo = update.message.photo[-1]
            file = await photo.get_file()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                await file.download_to_drive(temp_file.name)
                
                # Send to API
                async with aiohttp.ClientSession() as session:
                    with open(temp_file.name, 'rb') as f:
                        data = aiohttp.FormData()
                        data.add_field('telegram_id', telegram_id)
                        data.add_field('file', f, filename='receipt.jpg', content_type='image/jpeg')
                        
                        async with session.post(
                            f"{self.api_url}/okanassist/v1/process-receipt",
                            data=data
                        ) as response:
                            if response.status == 200:
                                result = await response.json()
                                await update.message.reply_text(result["message"], parse_mode='Markdown')
                            elif response.status == 401:
                                await update.message.reply_text(
                                    get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to process receipts!\nType /register to create your account.",
                                    parse_mode='Markdown'
                                )
                            else:
                                await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))
                
                # Cleanup
                os.unlink(temp_file.name)
                
        except Exception as e:
            print(f"❌ Error processing receipt: {e}")
            await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))

    async def handle_pdf_statement(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process bank statement PDFs with authentication"""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"📄 PDF statement from {user.first_name}")
        
        try:
            document = update.message.document
            file = await document.get_file()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                await file.download_to_drive(temp_file.name)
                
                # Send to API
                async with aiohttp.ClientSession() as session:
                    with open(temp_file.name, 'rb') as f:
                        data = aiohttp.FormData()
                        data.add_field('telegram_id', telegram_id)
                        data.add_field('file', f, filename=document.file_name, content_type='application/pdf')
                        
                        async with session.post(
                            f"{self.api_url}/okanassist/v1/process-bank-statement",
                            data=data
                        ) as response:
                            if response.status == 200:
                                result = await response.json()
                                await update.message.reply_text(result["message"], parse_mode='Markdown')
                            elif response.status == 401:
                                await update.message.reply_text(
                                    get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to process documents!\nType /register to create your account.",
                                    parse_mode='Markdown'
                                )
                            else:
                                await update.message.reply_text(get_message("generic_downtime", update.effective_user.language_code))
                
                # Cleanup
                os.unlink(temp_file.name)
                
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            await update.message.reply_text(get_message("generic_error", update.effective_user.language_code))

    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command with authentication"""
        user = update.effective_user
        telegram_id = str(user.id)
        print(f"👤 /profile command from {user.first_name}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/okanassist/v1/profile",
                    params={"telegram_id": telegram_id}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(result)
                        user_data = result.get("user_data", {})

                        # --- 2. Build and escape the message here ---
                        # Use escape_markdown(text, version=2) for V2 Markdown
                        email = escape_markdown(user_data.get('email', 'Not set'), version=2)
                        name = escape_markdown(user_data.get('name', 'Unknown'), version=2)
                        
                        language = escape_markdown(user_data.get('language', 'en'), version=2)
                        currency = escape_markdown(user_data.get('currency', 'USD'), version=2)
                        timezone = escape_markdown(user_data.get('timezone', 'UTC'), version=2)
                        premium_status = 'Yes' if user_data.get('is_premium') else 'No'

                        profile_message = get_message(
                            "profile_info", update.effective_user.language_code,
                            email=email,
                            name=name,
                            language=language,
                            currency=currency,
                            timezone=timezone,
                            webapp_url=self.app_url,
                            premium_status=premium_status
                        )
                        # FIX: Access manage_url from the top-level result, not user_data
                        manage_url = None
                        is_premium = user_data.get('is_premium', False)
                        if is_premium:
                            manage_url = result.get('manage_url', {}).get('portal_url', '')
                            profile_message += get_message("manage_url", update.effective_user.language_code, url=manage_url)+"\n\n"    
                        await update.message.reply_text(profile_message, parse_mode='MarkdownV2')
                    
                    elif response.status == 401:
                        await update.message.reply_text(
                            get_message("user_not_found", update.effective_user.language_code) + "\n\n🔐 You need to register first to view your profile!\nType /register to create your account.",
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text(
                            get_message("generic_error", update.effective_user.language_code)
                        )
        except Exception as e:
            print(f"❌ Error in profile command: {e}")
            await update.message.reply_text(get_message("generic_error", update.effective_user.language_code))
    
    async def set_commands(self, language_code="en"):
        """Set bot commands based on language"""
        lang_short = language_code.split('-')[0] if language_code else 'en'
        commands_data = MESSAGES.get(lang_short, MESSAGES['en']).get("commands", MESSAGES['en']["commands"])
        commands = [
            BotCommand(cmd["name"], cmd["description"])
            for cmd in commands_data.values()
        ]
        await self.app.bot.set_my_commands(commands)

    async def run(self):
        """Start the bot and HTTP server"""
        if not self.app:
            self.setup()
        
        await self.set_commands(language_code="en")
        
        print("🤖 Telegram Bot started!")
        print("🎯 Commands: /start, /register, /help, /balance, /reminders, /profile")
        print("📸 Send photos of receipts for automatic processing")
        print("📄 Send PDF bank statements for bulk transaction import")
        
        # Create a simple HTTP server for Cloud Run health checks
        async def health_check(request):
            return web.Response(text="Bot is running")
        
        web_app = web.Application()
        web_app.router.add_get('/health', health_check)
        
        # Get the port from environment (default 8080 for Cloud Run)
        port = int(os.getenv('PORT', 8080))
        
        # Start both the bot and the web server concurrently
        async with self.app:
            await self.app.start()
            await self.app.updater.start_polling()
            
            # Start the web server
            runner = web.AppRunner(web_app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', port)
            await site.start()
            print(f"🌐 HTTP server started on port {port}")
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping bot...")
            finally:
                await self.app.updater.stop()
                await self.app.stop()
                await runner.cleanup()

# --- Main block to run the bot ---
if __name__ == "__main__":
    bot = AgnoTelegramBot()
    asyncio.run(bot.run())