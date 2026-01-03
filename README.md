# 💰 Website Price Monitor Tool

Automated price monitoring tool for websites. Get alerts when prices drop below your target. Save time and money.

![Python](https://img.shields.io/badge/Python-3.14%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Multi-Product Monitoring**: Track unlimited products simultaneously
- **Automatic Price Checking**: Set check intervals (5, 15, or 60 minutes)
- **Target Price Alerts**: Get popup notifications when price drops
- **Persistent Storage**: Your monitors are saved and restored on restart
- **Real-time Updates**: See current prices and status at a glance
- **Activity Log**: Track all price checks and alerts

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/price-monitor-tool.git

# Install dependencies
pip install -r requirements.txt

# Run the tool
python price_monitor_tool.py
```

### Requirements

- Python 3.14+
- requests
- beautifulsoup4
- tkinter (usually included with Python)

## 📖 How to Use

1. **Add Monitor**:
   - Product Name: "iPhone 15 Pro"
   - Product URL: https://example.com/iphone-15
   - Price Selector: `.price` (CSS selector for price element)
   - Target Price: 999

2. **Set Check Interval**: Choose 5, 15, or 60 minutes

3. **Start Monitoring**: Click "Start Monitoring" button

4. **Get Alerts**: When price drops below target, you'll get a popup notification

### Finding CSS Selectors

1. Open website in Chrome
2. Right-click price → "Inspect"
3. Find the price element in DevTools
4. Note the class or id (e.g., `.product-price`, `#price`)

## 🎯 Use Cases

- Flight ticket price tracking
- Electronics sale monitoring
- Stock/crypto price alerts
- Real estate price watching
- Competitor price tracking

## ⚠️ CRITICAL DISCLAIMER

**This tool is provided "AS IS" without warranty of any kind.**

### Financial Responsibility
- **NOT A FINANCIAL ADVISOR** - This tool does NOT provide investment advice
- **No liability for financial decisions** made based on this tool
- Price information may be delayed, incorrect, or incomplete
- **You are solely responsible** for all purchases and investments

### Legal Compliance
- Check website Terms of Service before monitoring
- Some websites prohibit automated access
- Respect rate limits and robots.txt
- **The developer is not liable** for any legal issues

### Technical Limitations
- **Alerts may fail** due to network issues, website changes, or software bugs
- No guarantee of 100% uptime or accuracy
- Website structure changes will break monitoring
- Price parsing may fail or be incorrect
- Monitoring stops if program is closed or computer sleeps

### No Warranty
- **No guarantee of alert delivery** - you may miss price drops
- No guarantee that monitoring will work continuously
- No SLA or uptime commitment
- **Not responsible for missed opportunities** or financial losses

### Your Responsibility
- Verify all prices before making purchases
- Do not rely solely on this tool for time-sensitive decisions
- Understand that automated monitoring can fail
- Check websites manually as well
- This is a convenience tool, not a business-critical system

## 🛠️ Troubleshooting

**Problem**: "Element not found"
- **Solution**: CSS selector may be wrong. Use browser DevTools to find the correct selector.

**Problem**: Price shows as "N/A"
- **Solution**: Website structure may have changed. Update the CSS selector.

**Problem**: No alerts received
- **Solution**: Check that monitoring is running. Verify target price is set correctly.

**Problem**: Getting blocked by website
- **Solution**: Increase check interval. Some websites block frequent automated requests.

## 💡 Tips

- Use longer check intervals (60 min) to avoid blocking
- Test with "Check Now" button before starting automatic monitoring
- Keep the program running - monitoring stops when closed
- Don't monitor too many sites simultaneously

## ⚙️ Technical Details

- Monitors are saved in `price_monitors.json`
- Uses standard HTTP requests (User-Agent: Mozilla/5.0)
- No JavaScript rendering (static HTML only)
- Single-threaded monitoring loop

## 📝 License

MIT License - Use at your own risk. See LICENSE file for details.

## 🤝 Support

- This is a standalone tool delivered as-is
- For bugs or issues, please open a GitHub issue
- No ongoing support or maintenance included
- Website-specific selector issues cannot be debugged

## ⚡ Version

**Version 1.0.0** - Initial Release

### Known Limitations
- Does not work with JavaScript-rendered prices (React, Vue, etc.)
- Cannot bypass Cloudflare or anti-bot protection
- No email or SMS alerts (popup only)
- Monitoring stops when program is closed
- Maximum recommended: 10-20 products

---

**Built by Dumok Data Lab**

*Remember: This is a convenience tool, not a guarantee. Always verify prices manually before purchasing.*

## 🚫 What This Tool Is NOT

- ❌ Not a financial advisor or trading bot
- ❌ Not a guaranteed alert system
- ❌ Not for high-frequency trading
- ❌ Not a business-critical monitoring solution
- ❌ Not a replacement for manual price checking

**Use responsibly and at your own risk.**
