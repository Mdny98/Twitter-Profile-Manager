from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# --- Config ---
NUM_TWEETS = 100      # Max tweets to process
SLEEP_BETWEEN_ACTIONS = 2  # seconds
WAIT_TIMEOUT = 10     # seconds to wait for elements

# --- Setup Chrome with the session ---
options = Options()
options.add_argument("--user-data-dir=/tmp/chrome-twitter")  # Use a persistent Chrome session
options.add_argument("--profile-directory=Default")  
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

print('step1')
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# use your Username
driver.get("https://x.com/Username/likes")
time.sleep(5)

def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def wait_for_page_load():
    """Wait for the page to load properly"""
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        time.sleep(2)  # Additional wait for dynamic content
    except TimeoutException:
        print("Page load timeout - continuing anyway")

def unlike_visible_tweets():
    unliked = 0
    
    # Wait for page to load
    wait_for_page_load()
    
    # Try multiple selectors for unlike buttons
    selectors = [
        '//div[@data-testid="unlike"]',
        '//button[@data-testid="unlike"]',
        '//*[@data-testid="unlike"]',
        '//div[@aria-label="Unlike"]',
        '//button[@aria-label="Unlike"]',
        # Alternative approach - look for liked state buttons
        '//div[@data-testid="like"][@aria-pressed="true"]',
        '//button[@data-testid="like"][@aria-pressed="true"]'
    ]
    
    liked_buttons = []
    
    for selector in selectors:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            if buttons:
                liked_buttons = buttons
                print(f"Found {len(liked_buttons)} buttons with selector: {selector}")
                break
        except Exception as e:
            print(f"Error with selector {selector}: {e}")
            continue
    
    if not liked_buttons:
        print("No liked buttons found with any selector")
        # Debug: Print page source snippet
        try:
            articles = driver.find_elements(By.TAG_NAME, "article")
            print(f"Found {len(articles)} articles on page")
            if articles:
                # Look for any buttons in the first article
                first_article = articles[0]
                buttons = first_article.find_elements(By.TAG_NAME, "button")
                divs = first_article.find_elements(By.TAG_NAME, "div")
                print(f"First article has {len(buttons)} buttons and {len(divs)} divs")
                
                # Print some button attributes for debugging
                for i, btn in enumerate(buttons[:3]):  # First 3 buttons
                    try:
                        testid = btn.get_attribute("data-testid")
                        aria_label = btn.get_attribute("aria-label")
                        print(f"Button {i}: data-testid='{testid}', aria-label='{aria_label}'")
                    except:
                        pass
        except Exception as e:
            print(f"Debug error: {e}")
        
        return 0
    
    print(f'Found {len(liked_buttons)} liked buttons')
    
    for btn in liked_buttons:
        try:
            # Scroll to button to make sure it's visible
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.5)
            
            # Try clicking with JavaScript if regular click fails
            try:
                btn.click()
            except:
                driver.execute_script("arguments[0].click();", btn)
            
            time.sleep(SLEEP_BETWEEN_ACTIONS)
            unliked += 1
            print(f"Unliked tweet {unliked}")
            
            if unliked >= NUM_TWEETS:
                return unliked
                
        except Exception as e:
            print(f"Error unliking: {e}")
            continue
    
    return unliked

def undo_retweets_visible():
    undone = 0
    
    # Wait for page to load
    wait_for_page_load()
    
    # Try multiple selectors for unretweet buttons (first "Undo repost" button)
    selectors = [
        '//div[@data-testid="unretweet"]',
        '//button[@data-testid="unretweet"]',
        '//*[@data-testid="unretweet"]'
    ]
    
    retweet_buttons = []
    
    for selector in selectors:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            if buttons:
                retweet_buttons = buttons
                print(f"Found {len(retweet_buttons)} retweet buttons with selector: {selector}")
                break
        except Exception as e:
            continue
    
    if not retweet_buttons:
        print("No retweet buttons found")
        return 0
    
    for btn in retweet_buttons:
        try:
            # Scroll to button to make it visible
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)
            
            # Wait for any overlays to disappear
            time.sleep(0.5)
            
            # Try multiple approaches to click the first "Undo repost" button
            clicked = False
            
            # Method 1: Wait for element to be clickable and click
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))
                btn.click()
                clicked = True
                print("Clicked first 'Undo repost' button")
            except:
                pass
            
            # Method 2: JavaScript click if regular click failed
            if not clicked:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    clicked = True
                    print("Clicked first 'Undo repost' button with JavaScript")
                except:
                    pass
            
            # Method 3: Action chains click
            if not clicked:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(driver)
                    actions.move_to_element(btn).click().perform()
                    clicked = True
                    print("Clicked first 'Undo repost' button with ActionChains")
                except:
                    pass
            
            if not clicked:
                print("Could not click first retweet button, skipping...")
                continue
            
            time.sleep(1.5)  # Wait for menu to appear
            
            # Now look for the second "Undo repost" button in the menu (next to "Quote")
            confirm_selectors = [
                # Look for "Undo repost" text specifically
                '//div[@role="menuitem"][.//span[contains(text(),"Undo repost")]]',
                '//div[@role="menuitem"][.//span[text()="Undo repost"]]',
                '//span[contains(text(),"Undo repost")]/ancestor::div[@role="menuitem"]',
                '//span[text()="Undo repost"]/ancestor::div[@role="menuitem"]',
                # Alternative selectors
                '//div[@role="menuitem"][.//span[contains(text(),"Undo Repost")]]',
                '//div[@role="menuitem"][.//span[text()="Undo Repost"]]',
                # Look for the second option in menu items (usually Quote is first, Undo repost is second)
                '(//div[@role="menuitem"])[2]'
            ]
            
            confirm_btn = None
            for confirm_selector in confirm_selectors:
                try:
                    confirm_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, confirm_selector))
                    )
                    print(f"Found confirm button with selector: {confirm_selector}")
                    break
                except:
                    continue
            
            if confirm_btn:
                try:
                    # Try to click the second "Undo repost" button
                    confirm_btn.click()
                    print("Clicked second 'Undo repost' button")
                except:
                    # Try JavaScript click for confirm button too
                    driver.execute_script("arguments[0].click();", confirm_btn)
                    print("Clicked second 'Undo repost' button with JavaScript")
                
                time.sleep(SLEEP_BETWEEN_ACTIONS)
                undone += 1
                print(f"Successfully undid repost {undone}")
                
                if undone >= NUM_TWEETS:
                    return undone
            else:
                print("Could not find second 'Undo repost' button - checking what's available...")
                # Debug: print available menu items
                try:
                    menu_items = driver.find_elements(By.XPATH, '//div[@role="menuitem"]')
                    print(f"Found {len(menu_items)} menu items:")
                    for i, item in enumerate(menu_items):
                        try:
                            text = item.text.strip()
                            if text:
                                print(f"  Menu item {i}: '{text}'")
                        except:
                            pass
                    
                    # Also check for span elements with text
                    spans = driver.find_elements(By.XPATH, '//div[@role="menuitem"]//span')
                    print("Span texts in menu:")
                    for i, span in enumerate(spans[:10]):  # Limit to first 10
                        try:
                            text = span.text.strip()
                            if text:
                                print(f"  Span {i}: '{text}'")
                        except:
                            pass
                            
                except Exception as debug_error:
                    print(f"Debug error: {debug_error}")
                
                # Try to close menu by clicking elsewhere
                try:
                    driver.execute_script("document.body.click();")
                    time.sleep(0.5)
                except:
                    pass
                
        except Exception as e:
            print(f"Error unretweeting: {e}")
            # Try to close any open menus
            try:
                driver.execute_script("document.body.click();")
                time.sleep(0.5)
            except:
                pass
            continue
    
    return undone

# --- Process Likes ---
print("Unliking tweets...")
total_unliked = 0
attempts = 0
max_attempts = 20  # Prevent infinite loops

while total_unliked < NUM_TWEETS and attempts < max_attempts:
    attempts += 1
    print(f"Attempt {attempts}")
    
    unliked_this_round = unlike_visible_tweets()
    total_unliked += unliked_this_round
    
    if unliked_this_round == 0:
        print("No tweets unliked this round, scrolling...")
        scroll_down()
        time.sleep(3)  # Extra wait after scrolling
    else:
        print(f"Total unliked so far: {total_unliked}")

print(f"Finished unliking. Total: {total_unliked}")

# --- Process Retweets ---
driver.get("https://x.com/username")  # Replace with your actual username
time.sleep(5)

print("Undoing retweets...")
total_unretweeted = 0
attempts = 0

while total_unretweeted < NUM_TWEETS and attempts < max_attempts:
    attempts += 1
    print(f"Retweet attempt {attempts}")
    
    unretweeted_this_round = undo_retweets_visible()
    total_unretweeted += unretweeted_this_round
    
    if unretweeted_this_round == 0:
        print("No retweets undone this round, scrolling...")
        scroll_down()
        time.sleep(3)
    else:
        print(f"Total unretweeted so far: {total_unretweeted}")

print(f"✅ Done: Unliked {total_unliked}, Unretweeted {total_unretweeted}")
driver.quit()