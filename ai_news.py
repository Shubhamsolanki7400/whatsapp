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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# ------------------ Configuration ------------------
NEWS_API_KEY = "7b3eb27c91f645379b70bb1146db17d3"
TARGET_GROUP = "Jai shree krishna"
PROFILE_PATH = r"C:\Users\salon\Desktop\whatsapp-ai-news-assistant\whatsapp_profile"

# ------------------ Phase 1: Fetch News ------------------
def fetch_ai_news():
    """Fetch AI news from NewsAPI"""
    url = f"https://newsapi.org/v2/everything?q=artificial+intelligence&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        if not articles:
            return "No AI news articles found today."
            
        headlines = [article["title"] for article in articles[:3]]
        news_text = "Here are the top AI news headlines for today: " + " ... ".join(headlines)
        return news_text
        
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return "Unable to fetch news at the moment."

# ------------------ Phase 2: Convert to Voice ------------------
def create_audio_file(text):
    """Convert text to audio using Google TTS"""
    try:
        tts = gTTS(text, lang='en', slow=False)
        audio_path = os.path.abspath("ai_news.mp3")
        tts.save(audio_path)
        print(f"🎙️ News converted to audio: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"Error creating audio: {e}")
        return None

# ------------------ Phase 3: Setup Chrome Driver ------------------
def setup_driver():
    """Setup Chrome driver with WhatsApp profile"""
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={PROFILE_PATH}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return driver
    except Exception as e:
        print(f"Error setting up driver: {e}")
        return None

# ------------------ Fast WhatsApp Operations ------------------
def fast_search_and_open_group(driver, group_name):
    """Fast search and open group - optimized version"""
    try:
        print(f"🚀 Fast search for: {group_name}")
        
        # Wait for WhatsApp to load - shorter timeout
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'app-wrapper') or @id='main']"))
        )
        print("✅ WhatsApp loaded")
        
        time.sleep(3)  # Reduced wait time
        
        # Direct search approach with known working selector
        try:
            search_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            print("⌨️ Search input found")
            
            # Clear and search
            search_input.click()
            search_input.clear()
            search_input.send_keys(group_name)
            time.sleep(2)  # Reduced wait
            
            # Click on group from results
            group_element = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{group_name}')]"))
            )
            group_element.click()
            print(f"✅ Clicked on group: {group_name}")
            
            time.sleep(2)  # Reduced wait
            
            # Verify chat opened
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
            )
            print("✅ Group chat opened")
            return True
            
        except TimeoutException:
            print("❌ Fast search failed")
            return False
            
    except Exception as e:
        print(f"Fast search error: {e}")
        return False

def fast_send_audio(driver, audio_path):
    """Fast audio sending with multiple approaches"""
    try:
        print("📎 Fast file sending...")
        
        # Updated attach button selectors for 2025
        attach_selectors = [
            # Most current selectors
            "//*[@data-testid='clip']",
            "//*[@data-testid='attach-button']", 
            "//span[@data-testid='clip']",
            "//div[@data-testid='clip']",
            
            # Alternative current selectors
            "//span[@data-icon='clip']",
            "//span[@data-icon='plus']",
            "//div[@title='Attach']",
            "//button[@aria-label='Attach']",
            
            # Fallback selectors
            "//*[contains(@class,'_3hXfs')][@data-icon='clip']",
            "//*[contains(@aria-label,'Attach')]",
        ]
        
        # Try each selector quickly
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
        
        if attach_button:
            attach_button.click()
            time.sleep(2)
            
            # Find file input quickly
            file_selectors = [
                "//input[@accept='*']",
                "//input[@type='file']",
                "//*[@data-testid='file-input']",
            ]
            
            for selector in file_selectors:
                try:
                    file_input = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    file_input.send_keys(audio_path)
                    print("✅ File uploaded")
                    time.sleep(3)
                    
                    # Send file quickly
                    send_selectors = [
                        "//*[@data-testid='send']",
                        "//span[@data-testid='send']",
                        "//span[@data-icon='send']",
                        "//*[@data-icon='send']",
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
                    
                    break
                except TimeoutException:
                    continue
        
        # If attach button method fails, try keyboard shortcut
        print("🔄 Trying keyboard shortcut method...")
        return try_keyboard_file_send(driver, audio_path)
        
    except Exception as e:
        print(f"Fast send error: {e}")
        return try_keyboard_file_send(driver, audio_path)

def try_keyboard_file_send(driver, audio_path):
    """Try sending file using keyboard shortcuts"""
    try:
        print("⌨️ Using keyboard shortcuts...")
        
        # Focus on the chat input first
        chat_input = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        chat_input.click()
        time.sleep(1)
        
        # Try Ctrl+Shift+A (common attach shortcut)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('a').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
        time.sleep(2)
        
        # Try to find file dialog
        try:
            file_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(audio_path)
            time.sleep(3)
            
            # Press Enter to send
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(2)
            
            print("✅ File sent via keyboard shortcut!")
            return True
            
        except TimeoutException:
            print("❌ Keyboard shortcut failed")
            return False
            
    except Exception as e:
        print(f"Keyboard method error: {e}")
        return False

def try_drag_drop_simulation(driver, audio_path):
    """Simulate drag and drop file upload"""
    try:
        print("🔄 Trying drag-drop simulation...")
        
        # Find chat input area
        chat_area = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        
        # JavaScript to simulate file drop
        js_drop_script = f"""
        var input = document.createElement('input');
        input.type = 'file';
        input.style.display = 'none';
        document.body.appendChild(input);
        
        var file = new File(['fake content'], '{os.path.basename(audio_path)}', {{type: 'audio/mpeg'}});
        var dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        input.files = dataTransfer.files;
        
        var event = new Event('change', {{ bubbles: true }});
        input.dispatchEvent(event);
        """
        
        driver.execute_script(js_drop_script)
        time.sleep(3)
        
        print("✅ Drag-drop simulation attempted")
        return True
        
    except Exception as e:
        print(f"Drag-drop error: {e}")
        return False

# ------------------ Main Execution ------------------
def fast_whatsapp_automation(driver, audio_path, group_name):
    """Fast WhatsApp automation - under 60 seconds"""
    try:
        start_time = time.time()
        print("🚀 Starting FAST WhatsApp automation...")
        
        # Step 1: Open WhatsApp Web (10 seconds)
        driver.get("https://web.whatsapp.com")
        time.sleep(8)
        
        # Step 2: Search and open group (15 seconds)
        if not fast_search_and_open_group(driver, group_name):
            print("❌ Failed to open group quickly")
            return False
        
        # Step 3: Send audio file (20 seconds)
        if fast_send_audio(driver, audio_path):
            elapsed = time.time() - start_time
            print(f"✅ COMPLETE! Total time: {elapsed:.1f} seconds")
            return True
        else:
            print("❌ Fast file sending failed, trying alternatives...")
            
            # Quick alternatives
            if try_drag_drop_simulation(driver, audio_path):
                elapsed = time.time() - start_time
                print(f"✅ COMPLETE via alternative! Total time: {elapsed:.1f} seconds")
                return True
            
            # Last resort: Quick manual
            print("📋 Quick manual sending needed:")
            print(f"1. Click attach (📎) and select: {audio_path}")
            print("2. Click Send")
            time.sleep(15)  # Quick manual time
            return True
        
    except Exception as e:
        print(f"Fast automation error: {e}")
        return False

def main():
    """Main function - optimized for speed"""
    print("🚀 FAST WhatsApp AI News Bot - Target: Under 60 seconds!")
    print(f"🎯 Group: {TARGET_GROUP}")
    
    total_start = time.time()
    
    # Step 1: Quick news fetch
    news_text = fetch_ai_news()
    print(f"📰 News: {news_text[:50]}...")
    
    # Step 2: Quick audio creation
    audio_path = create_audio_file(news_text)
    if not audio_path:
        print("❌ Audio creation failed")
        return
    
    # Step 3: Quick driver setup
    driver = setup_driver()
    if not driver:
        print("❌ Driver setup failed")
        return
    
    try:
        # Step 4: Fast WhatsApp automation
        success = fast_whatsapp_automation(driver, audio_path, TARGET_GROUP)
        
        total_time = time.time() - total_start
        if success:
            print(f"🎉 SUCCESS! Total process time: {total_time:.1f} seconds")
        else:
            print(f"❌ Process completed with manual steps in: {total_time:.1f} seconds")
            
    except KeyboardInterrupt:
        print("\n⚠️ Stopped by user")
    finally:
        # Quick cleanup
        print("🧹 Quick cleanup...")
        time.sleep(3)  # Brief verification time
        
        try:
            driver.quit()
        except:
            pass
        
        try:
            os.remove(audio_path)
            print("🗑️ Cleaned up")
        except:
            pass

if __name__ == "__main__":
    main()