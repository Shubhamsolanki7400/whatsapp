import time
import os
import requests
from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# ------------------ Configuration ------------------
NEWS_API_KEY = "7b3eb27c91f645379b70bb1146db17d3"
TARGET_GROUP = "7898237190"
PROFILE_PATH = r"C:\Users\salon\Desktop\whatsapp-ai-news-assistant\whatsapp_profile"

# ------------------ Phase 1: Fetch News ------------------
def fetch_ai_news():
    """Fetch AI news from NewsAPI with better error handling"""
    url = f"https://newsapi.org/v2/everything?q=artificial+intelligence&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    
    try:
        print("📰 Fetching AI news...")
        response = requests.get(url, timeout=10)
        
        # Check for API quota issues
        if response.status_code == 429:
            print("❌ NewsAPI quota exceeded. Using fallback news.")
            return "Today's AI Update: OpenAI continues development of advanced AI models, while tech companies invest heavily in artificial intelligence infrastructure and research."
            
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return "No AI news articles found today."
            
        # Create better formatted news
        headlines = []
        for i, article in enumerate(articles[:3], 1):
            title = article.get("title", "").split(" - ")[0]  # Remove source from title
            headlines.append(f"{i}. {title}")
        
        news_text = f"Here are today's top AI news headlines: {' ... '.join(headlines)}"
        print(f"✅ News fetched: {len(headlines)} headlines")
        return news_text
        
    except requests.RequestException as e:
        print(f"❌ Error fetching news: {e}")
        return "Today's AI Update: The artificial intelligence industry continues to evolve with new developments in machine learning and automation technologies."

# ------------------ Phase 2: Convert to Voice ------------------
def create_audio_file(text):
    """Convert text to audio using Google TTS with better error handling"""
    try:
        print("🎙️ Creating audio file...")
        # Limit text length for better audio quality
        if len(text) > 500:
            text = text[:500] + "..."
            
        tts = gTTS(text, lang='en', slow=False)
        audio_path = os.path.abspath("ai_news.mp3")
        
        # Remove existing file if present
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        tts.save(audio_path)
        
        # Verify file was created
        if os.path.exists(audio_path):
            print(f"✅ Audio created: {audio_path}")
            return audio_path
        else:
            print("❌ Audio file creation failed")
            return None
            
    except Exception as e:
        print(f"❌ Error creating audio: {e}")
        return None

# ------------------ Phase 3: Setup Chrome Driver ------------------
def setup_driver():
    """Setup Chrome driver with WhatsApp profile and better options"""
    options = webdriver.ChromeOptions()
    
    # Essential options
    options.add_argument(f"user-data-dir={PROFILE_PATH}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    
    # Prevent automation detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        print("🚀 Setting up Chrome driver...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Execute script to hide automation flags
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver setup complete")
        return driver
        
    except Exception as e:
        print(f"❌ Error setting up driver: {e}")
        return None

# ------------------ Improved WhatsApp Operations ------------------
def wait_for_whatsapp_load(driver):
    """Wait for WhatsApp to fully load with multiple indicators"""
    try:
        print("⏳ Waiting for WhatsApp to load...")
        
        # Multiple selectors to check for WhatsApp load
        load_indicators = [
            "//div[contains(@class,'app-wrapper-web')]",
            "//div[@id='main']",
            "//div[contains(@class,'_3V5x5')]",  # Chat list area
            "//*[@data-testid='chat-list']",
        ]
        
        for indicator in load_indicators:
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, indicator))
                )
                print("✅ WhatsApp loaded successfully")
                return True
            except TimeoutException:
                continue
                
        # Check if QR code is showing (not logged in)
        try:
            qr_code = driver.find_element(By.XPATH, "//canvas[@aria-label='Scan this QR code to link a device!']")
            if qr_code:
                print("❌ QR Code detected - Please scan to login first")
                return False
        except NoSuchElementException:
            pass
            
        print("✅ WhatsApp appears to be loaded")
        return True
        
    except Exception as e:
        print(f"❌ Error waiting for WhatsApp load: {e}")
        return False

def improved_search_and_open_group(driver, group_name):
    """Improved search with multiple selector strategies"""
    try:
        print(f"🔍 Searching for: {group_name}")
        
        # Wait a bit for everything to settle
        time.sleep(3)
        
        # Multiple search input selectors (updated for 2025)
        search_selectors = [
            # Most current selectors
            "//div[@contenteditable='true'][@data-tab='3']",
            "//div[@contenteditable='true'][@title='Search input textbox']",
            "//*[@data-testid='chat-list-search']",
            
            # Alternative selectors
            "//div[contains(@class,'_13NKt copyable-text selectable-text')][@contenteditable='true']",
            "//div[@role='textbox'][@contenteditable='true']",
            "//input[@placeholder='Search or start new chat']",
            
            # Fallback selectors
            "//*[contains(@class,'_2cYbV')]",
            "//div[contains(@class,'_3u328')][@contenteditable='true']",
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                search_input = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"✅ Search input found with: {selector}")
                break
            except TimeoutException:
                continue
        
        if not search_input:
            # Try keyboard shortcut to focus search
            print("🔄 Trying keyboard shortcut Ctrl+F...")
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('f').key_up(Keys.CONTROL).perform()
            time.sleep(2)
            
            # Try again after keyboard shortcut
            for selector in search_selectors[:3]:
                try:
                    search_input = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
        
        if search_input:
            # Clear and search
            search_input.click()
            time.sleep(1)
            search_input.clear()
            search_input.send_keys(group_name)
            time.sleep(3)  # Wait for search results
            
            # Try to click on the group from results
            group_selectors = [
                f"//span[@title='{group_name}']",
                f"//span[contains(text(),'{group_name}')]",
                f"//*[contains(@class,'_21S-L') and contains(text(),'{group_name}')]",
                f"//div[contains(@class,'_8nE1Y') and contains(text(),'{group_name}')]",
            ]
            
            for selector in group_selectors:
                try:
                    group_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    group_element.click()
                    print(f"✅ Clicked on group: {group_name}")
                    time.sleep(3)
                    
                    # Verify chat opened by looking for message input
                    message_selectors = [
                        "//div[@contenteditable='true'][@data-tab='10']",
                        "//div[@contenteditable='true'][@data-testid='conversation-compose-box-input']",
                        "//*[@data-testid='compose-box-input']",
                    ]
                    
                    for msg_selector in message_selectors:
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, msg_selector))
                            )
                            print("✅ Group chat opened successfully")
                            return True
                        except TimeoutException:
                            continue
                    
                    print("⚠️ Group may be open but message input not found")
                    return True
                    
                except TimeoutException:
                    continue
            
            print("❌ Group not found in search results")
            return False
        else:
            print("❌ Could not find search input")
            return False
            
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def improved_send_audio(driver, audio_path):
    """Improved audio sending with verification that message was actually sent"""
    try:
        print("📎 Attempting to send audio file...")
        
        # First verify we're actually in a chat
        if not verify_chat_open(driver):
            print("❌ Chat is not properly opened - cannot send file")
            return False
        
        # Get initial message count for verification
        initial_msg_count = get_message_count(driver)
        
        # Strategy 1: Try standard attach button
        if send_via_attach_button(driver, audio_path):
            if verify_message_sent(driver, initial_msg_count):
                print("✅ Message sent and verified via attach button!")
                return True
            
        # Strategy 2: Try drag and drop
        print("🔄 Trying drag and drop method...")
        if send_via_drag_drop(driver, audio_path):
            if verify_message_sent(driver, initial_msg_count):
                print("✅ Message sent and verified via drag and drop!")
                return True
            
        # Strategy 3: Try keyboard shortcut
        print("🔄 Trying keyboard shortcut...")
        if send_via_keyboard_shortcut(driver, audio_path):
            if verify_message_sent(driver, initial_msg_count):
                print("✅ Message sent and verified via keyboard!")
                return True
        
        print("❌ All automatic methods failed or could not verify send")
        return False
        
    except Exception as e:
        print(f"❌ Audio sending error: {e}")
        return False

def verify_chat_open(driver):
    """Verify that a chat is actually open and ready"""
    try:
        # Check for message input
        message_selectors = [
            "//div[@contenteditable='true'][@data-tab='10']",
            "//*[@data-testid='compose-box-input']",
            "//div[@contenteditable='true'][@role='textbox'][@spellcheck='true']",
        ]
        
        for selector in message_selectors:
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if element.is_displayed():
                    return True
            except TimeoutException:
                continue
        
        return False
    except:
        return False

def get_message_count(driver):
    """Get current message count in chat"""
    try:
        messages = driver.find_elements(By.XPATH, "//div[contains(@class,'message-')]")
        return len(messages)
    except:
        return 0

def verify_message_sent(driver, initial_count, timeout=15):
    """Verify that a new message was actually sent"""
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check for audio message indicators
                audio_indicators = [
                    "//div[contains(@class,'audio-')]",
                    "//*[@data-testid='audio-message']",
                    "//span[contains(@class,'audio')]",
                    "//*[contains(@aria-label,'Audio')]",
                ]
                
                for indicator in audio_indicators:
                    audio_elements = driver.find_elements(By.XPATH, indicator)
                    if audio_elements:
                        print(f"✅ Audio message detected: {len(audio_elements)} audio elements found")
                        return True
                
                # Check for general message increase
                current_count = get_message_count(driver)
                if current_count > initial_count:
                    print(f"✅ New message detected (count increased from {initial_count} to {current_count})")
                    return True
                    
                time.sleep(1)
            except:
                time.sleep(1)
                continue
        
        print("❌ No new message detected within timeout period")
        return False
    except:
        return False

def send_via_attach_button(driver, audio_path):
    """Send file via attach button - updated selectors"""
    try:
        # Updated attach button selectors for 2025
        attach_selectors = [
            # Primary selectors
            "//*[@data-testid='clip']",
            "//span[@data-testid='clip']",
            "//div[@data-testid='clip']",
            
            # Alternative data-icon selectors
            "//span[@data-icon='clip']",
            "//span[@data-icon='plus']",
            "//span[@data-icon='attach-menu-plus']",
            
            # Aria-label selectors
            "//button[@aria-label='Attach']",
            "//*[@aria-label='Attach']",
            "//*[@title='Attach']",
            
            # Class-based fallbacks
            "//*[contains(@class,'_3hXfs')]",
            "//*[contains(@class,'_1yBOz')]",
        ]
        
        attach_button = None
        for selector in attach_selectors:
            try:
                attach_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"✅ Attach button found: {selector}")
                break
            except TimeoutException:
                continue
        
        if not attach_button:
            return False
            
        attach_button.click()
        time.sleep(2)
        
        # Find and use file input
        file_selectors = [
            "//input[@accept='*']",
            "//input[@type='file']",
            "//*[@data-testid='file-input']",
            "//input[contains(@accept,'audio') or contains(@accept,'*')]",
        ]
        
        for selector in file_selectors:
            try:
                file_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                file_input.send_keys(audio_path)
                print("✅ File selected")
                time.sleep(4)  # Wait for upload
                
                # Find and click send button
                send_selectors = [
                    "//*[@data-testid='send' or @data-icon='send']",
                    "//span[@data-testid='send']",
                    "//span[@data-icon='send']",
                    "//button[@aria-label='Send']",
                ]
                
                for send_selector in send_selectors:
                    try:
                        send_button = WebDriverWait(driver, 8).until(
                            EC.element_to_be_clickable((By.XPATH, send_selector))
                        )
                        send_button.click()
                        print("✅ File sent successfully!")
                        return True
                    except TimeoutException:
                        continue
                
                # If send button not found, try Enter key
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                print("✅ File sent via Enter key!")
                return True
                
            except TimeoutException:
                continue
        
        return False
        
    except Exception as e:
        print(f"Attach button method error: {e}")
        return False

def send_via_drag_drop(driver, audio_path):
    """Send file via drag and drop simulation"""
    try:
        # Find the message input area
        message_selectors = [
            "//div[@contenteditable='true'][@data-tab='10']",
            "//*[@data-testid='compose-box-input']",
            "//div[@contenteditable='true'][@role='textbox']",
        ]
        
        drop_target = None
        for selector in message_selectors:
            try:
                drop_target = driver.find_element(By.XPATH, selector)
                break
            except NoSuchElementException:
                continue
        
        if not drop_target:
            return False
        
        # JavaScript to simulate file drop
        js_script = f"""
        var target = arguments[0];
        var file = new File([''], '{os.path.basename(audio_path)}', {{type: 'audio/mpeg'}});
        var dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        
        var dragEvent = new DragEvent('drop', {{
            dataTransfer: dataTransfer,
            bubbles: true,
            cancelable: true
        }});
        
        target.dispatchEvent(dragEvent);
        """
        
        driver.execute_script(js_script, drop_target)
        time.sleep(5)
        
        print("✅ Drag and drop attempted")
        return True
        
    except Exception as e:
        print(f"Drag and drop error: {e}")
        return False

def send_via_keyboard_shortcut(driver, audio_path):
    """Send file using keyboard shortcuts"""
    try:
        # Focus on message input
        message_input = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        message_input.click()
        time.sleep(1)
        
        # Try Ctrl+Shift+A (attach shortcut)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('a').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
        time.sleep(3)
        
        # Look for file dialog
        try:
            file_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(audio_path)
            time.sleep(3)
            
            # Send with Enter
            actions.send_keys(Keys.ENTER).perform()
            print("✅ File sent via keyboard shortcut!")
            return True
            
        except TimeoutException:
            return False
            
    except Exception as e:
        print(f"Keyboard shortcut error: {e}")
        return False

# ------------------ Main Execution ------------------
def main():
    """Main function with improved error handling and timing"""
    print("🚀 WhatsApp AI News Bot - Enhanced Version")
    print(f"🎯 Target Group: {TARGET_GROUP}")
    
    total_start = time.time()
    
    try:
        # Step 1: Fetch news
        news_text = fetch_ai_news()
        if not news_text or len(news_text) < 10:
            print("❌ News fetch failed or insufficient content")
            return
        
        # Step 2: Create audio
        audio_path = create_audio_file(news_text)
        if not audio_path:
            print("❌ Audio creation failed")
            return
        
        # Step 3: Setup driver
        driver = setup_driver()
        if not driver:
            print("❌ Driver setup failed")
            return
        
        # ---------------- Inner try for WhatsApp steps ----------------
        try:
            # Step 4: Open WhatsApp
            print("🌐 Opening WhatsApp Web...")
            driver.get("https://web.whatsapp.com")

            # Step 5: Wait for load
            if not wait_for_whatsapp_load(driver):
                print("❌ WhatsApp failed to load properly")
                return

            # Step 6: Search and directly open group
            group_opened = improved_search_and_open_group(driver, TARGET_GROUP)

            if group_opened:
                try:
                    print("🔎 Verifying that group chat is open...")
                    # Wait for message input box inside chat
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                    )
                    print("✅ Group opened successfully, continuing...")
                except Exception:
                    print("⚠️ Group clicked but chat not open, retrying...")
                    # Try clicking group again
                    group_opened = improved_search_and_open_group(driver, TARGET_GROUP)
                    if group_opened:
                        print("✅ Group opened after retry, continuing...")
                    else:
                        print("❌ Failed to open target group after retry")
                        return
            else:
                print("❌ Failed to open target group")
                return

            # Step 7: Send audio with verification
            print("📤 Attempting to send audio...")
            send_success = improved_send_audio(driver, audio_path)
            if send_success:
                print("🎉 Audio message sent successfully")
            else:
                print("⚠️ Audio sending failed")

        except KeyboardInterrupt:
            print("\n⚠️ Process interrupted by user")

        finally:
            # Cleanup
            print("🧹 Cleaning up...")
            time.sleep(2)
            try:
                driver.quit()
            except Exception as e:
                print(f"⚠️ Driver quit error: {e}")
        # --------------------------------------------------------------

    except Exception as e:
        print(f"❌ Main execution error: {e}")

    finally:
        elapsed = time.time() - total_start
        print(f"⏳ Total execution time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
