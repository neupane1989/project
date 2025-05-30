import os
import re

HTML_DIR = "html"

def rewrite_content(content):
    # Branding replacements
    content = re.sub(r'adminuiux', 'i Investment', content, flags=re.IGNORECASE)
    content = re.sub(r'InvestmentUX|UX\b', 'i Investment', content)
    content = re.sub(r'company-tagline[^>]*>[^<]*', 'company-tagline">Your future, Your security', content)
    content = re.sub(r'Web and Mobile HTML template', 'Your future, Your security', content, flags=re.IGNORECASE)
    content = re.sub(r'AdminUIUX HTML template', 'Your future, Your security', content, flags=re.IGNORECASE)
    content = re.sub(r'adminuiux\.com', 'iinvestment.com', content, flags=re.IGNORECASE)

    # Currencies
    content = re.sub(r'\$\s?([0-9,.]+)', r'د.إ \1', content)
    content = re.sub(r'\bUSD\b', 'AED', content)
    content = re.sub(r'\bdollar(s)?\b', 'AED', content, flags=re.IGNORECASE)

    # Replace hardcoded demo content for dashboard
    content = re.sub(r'(?s)<!-- Welcome box -->.*?<!-- total profit -->', """
<!-- Welcome box -->
<div class="row align-items-center">
    <div class="col-12 col-lg mb-4">
        <h3 class="fw-normal mb-0 text-secondary">Good Morning,</h3>
        <h1>Welcome to i Investment</h1>
        <p>Your trusted partner for investment and insurance solutions in the UAE. Manage your wealth, insure your future, and plan your financial goals efficiently with us.</p>
    </div>
    <!-- Wallet Balance in AED -->
    <div class="col-6 col-lg-3 col-xl-2 mb-4">
        <div class="card iinvestment-card">
            <div class="card-body">
                <p class="text-secondary small mb-2">Wallet Balance</p>
                <h4 class="mb-3">د.إ 52,300</h4>
                <span class="badge badge-light text-bg-success"><i class="me-1 bi bi-arrow-up-short"></i>Updated</span>
            </div>
        </div>
    </div>
    <!-- Insurance Premiums -->
    <div class="col-6 col-lg-3 col-xl-2 mb-4">
        <div class="card iinvestment-card">
            <div class="card-body">
                <p class="text-secondary small mb-2">Insurance Premiums</p>
                <h4 class="mb-3">د.إ 1,800</h4>
                <span class="badge badge-light text-bg-info"><i class="me-1 bi bi-shield-check"></i>Active</span>
            </div>
        </div>
    </div>
</div>
<!-- total profit -->""", content)

    # Remove demo/template phrases like "Buy Now", "Demo", "Template", "Sample", etc.
    content = re.sub(r'(Buy Now|Demo|Sample|Template)[^<\n]*', 'Contact Us', content, flags=re.IGNORECASE)
    content = re.sub(r'accounting|inventory|social|tracking|network|directory|learning|project', '', content, flags=re.IGNORECASE)

    # Portfolio, Insurance, Statistics, etc.
    content = re.sub(r'(?s)<!-- Main investment/insurance content goes here -->.*?<!-- Standard footer -->', """
<!-- Main investment/insurance content goes here -->
<div class="container mt-4" id="main-content">
    <h2>Grow and Protect Your Wealth</h2>
    <p>At i Investment, we offer:</p>
    <ul>
        <li>Personalized Investment Planning for UAE residents and expatriates</li>
        <li>Comprehensive insurance: life, health, property, and business protection</li>
        <li>Goal-based wealth management tools</li>
        <li>Regular portfolio performance updates in AED</li>
        <li>Secure digital wallet for seamless transactions</li>
    </ul>
    <p>Contact our certified advisors to start your journey toward financial security and growth.</p>
</div>
<!-- Standard footer -->""", content)

    # Remove any remaining hardcoded/dummy data not fitting investment/insurance context
    content = re.sub(r'(?s)<!--.*?(demo|template|sample|showcase).*?-->', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\b[0-9]{1,2}:[0-9]{2} (am|pm)\b', '', content, flags=re.IGNORECASE)
    content = re.sub(r'(?i)Congratulations?[^<\n]*', '', content) # Remove demo notifications

    # Replace statistics, charts, etc. with investment/insurance context
    content = re.sub(r'(?s)<!-- Summary chart -->.*?<!-- updates -->', """
<!-- Portfolio Summary -->
<div class="row">
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-body">
                <h5>Portfolio Value</h5>
                <p>Monitor the value of your investments across mutual funds, stocks, and bonds.</p>
                <h4>د.إ 120,000</h4>
            </div>
        </div>
    </div>
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-body">
                <h5>Insurance Overview</h5>
                <p>Overview of your active insurance policies and upcoming renewals.</p>
                <ul>
                    <li>Life Insurance: Active</li>
                    <li>Health Insurance: Active</li>
                    <li>Car Insurance: Expires in 3 months</li>
                </ul>
            </div>
        </div>
    </div>
</div>
<!-- updates -->""", content)

    # Remove any remaining content that looks like a template/demo table, fake statistics, or unrelated features
    content = re.sub(r'(?s)<table.*?</table>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'(?s)<figure.*?</figure>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'(?s)<div class="swiper[^>]*>.*?</div>', '', content, flags=re.IGNORECASE)

    # Footer
    content = re.sub(
        r'Copyright ?@?[0-9, ]*,? ?[A-Za-z ]+by[^<]*',
        'Copyright ©2024, i Investment. Your future, Your security.',
        content
    )

    return content

def process_html_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        original = f.read()
    updated = rewrite_content(original)
    if original != updated:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Updated: {filepath}")

def main():
    for root, dirs, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith(".html"):
                process_html_file(os.path.join(root, file))

if __name__ == "__main__":
    main()