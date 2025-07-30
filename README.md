# Twitter Profile Manager

A collection of Python scripts for managing Twitter account interactions, specifically for unliking posts and undoing retweets (unretweets). This repository provides two different approaches: one using the official Twitter API and another using browser automation with Selenium.

## Features

- **Unlike posts**: Remove likes from previously liked tweets
- **Undo retweets**: Remove retweets from your profile
- **Two implementation methods**:
  - API-based approach using Twitter API v2
  - Browser automation using Selenium WebDriver

## Scripts Overview

### 1. `app.py` - Twitter API Implementation
Uses the official Twitter API to perform bulk operations on your account.

**Advantages:**
- Fast and efficient
- No browser dependencies
- Rate limiting handled by API
- More reliable for large-scale operations

**Requirements:**
- Twitter API credentials (Bearer Token, API Key, etc.)
- Twitter Developer Account

### 2. `app-selenium.py` - Selenium Implementation
Uses browser automation to simulate user interactions on Twitter's web interface.

**Advantages:**
- No API credentials required
- Works with regular Twitter account
- Can handle operations not available through API

**Requirements:**
- Chrome/Firefox browser
- WebDriver executable
- Stable internet connection

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Clone the Repository
```bash
git clone https://github.com/yourusername/Twitter-Profile-Manager.git
cd Twitter-Profile-Manager
```

### Install Dependencies

For API-based script:
```bash
pip install tweepy requests python-dotenv
```

For Selenium-based script:
```bash
pip install selenium webdriver-manager python-dotenv
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### API Method Setup (`app.py`)

1. Create a Twitter Developer Account at [developer.twitter.com](https://developer.twitter.com)
2. Create a new app and generate your credentials
3. Create a `.env` file in the project root:

```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

### Selenium Method Setup

1. Create a `.env` file with your Twitter credentials:

```env
TWITTER_USERNAME=your_username_or_email
TWITTER_PASSWORD=your_password
```

2. The script will automatically download the appropriate WebDriver

## Usage

### Using the API Method
```bash
python app.py
```

### Using the Selenium Method
```bash
python app-selenium.py
```



## Safety Features

- **Rate limiting**: Both scripts include delays to avoid hitting Twitter's rate limits
- **Confirmation prompts**: Scripts ask for confirmation before performing bulk operations
- **Progress tracking**: Real-time feedback on operation progress
- **Error handling**: Graceful handling of network issues and API errors
- **Dry run mode**: Test the script without making actual changes

## Rate Limits

### API Method
- Follows Twitter's official rate limits
- Automatic retry with exponential backoff
- Respects the 15-minute rate limit windows

### Selenium Method
- Includes randomized delays between actions
- Configurable wait times to avoid detection
- Automatic handling of loading delays


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Legal and Ethical Considerations

- Use these scripts responsibly and in accordance with Twitter's Terms of Service
- Respect rate limits to avoid account suspension
- Be mindful of Twitter's automation rules
- Consider the impact on your followers when performing bulk operations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with Twitter's Terms of Service and applicable laws. The authors are not responsible for any account suspensions or other consequences resulting from the use of these scripts.

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/twitter-account-manager/issues) page
2. Create a new issue with detailed information about your problem
3. Include relevant error messages and system information

## Changelog

### v1.0.0
- Initial release with API and Selenium implementations
- Support for unliking posts and undoing retweets
- Basic error handling and rate limiting

---

**Note**: Always test scripts on a small scale before running large operations. Keep your API credentials secure and never commit them to version control.
