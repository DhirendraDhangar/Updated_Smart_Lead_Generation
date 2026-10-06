import requests
from bs4 import BeautifulSoup
import re
import time
TIMEOUT = 5
HEADERS = {"User-Agent": "Mozilla/5.0"}
def analyze_website(url):
    issues = []
    services = set()
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        # ONLY ONE REQUEST
        start = time.time()
        r = requests.get(url, headers = HEADERS, timeout = TIMEOUT)
        load_time = time.time() - start
        soup = BeautifulSoup(r.text, "html.parser")
        performance = 100
        mobile = 100
        # 1. PERFORMANCE
        # --------------------------------
        if load_time > 4:
            performance -= 25
            issues.append(f"Slow page load ({load_time:.1f}s)")
            services.add("Web Development")
        elif load_time > 2:
            performance -= 10
            issues.append(f"Page load needs improvement ({load_time:.1f}s)")
            services.add("Web Development")
        # Get resources ONCE
        images = soup.find_all("img")
        css = soup.find_all("link", rel="stylesheet")
        scripts = soup.find_all("script")
        image_count = len(images)
        css_count = len(css)
        js_count = len(scripts)
        # Image optimization
        if image_count > 30:
            performance -= 10
            issues.append("High number of images")
            services.add("Web Development")
        if image_count > 5:
            lazy = sum(
                img.get("loading") == "lazy"
                for img in images)
            if lazy == 0:
                performance -= 5
                issues.append("Image lazy loading not detected")
                services.add("Web Development")
        # CSS / JS
        if css_count > 15:
            performance -= 5
            issues.append("Excessive CSS resources")
            services.add("Web Development")

        if js_count > 30:
            performance -= 5
            issues.append("Excessive JavaScript resources")
            services.add("Web Development")

        # HTTP requests approximation
        requests_count = (image_count + css_count +js_count + len(soup.find_all("iframe")))
        if requests_count > 60:
            performance -= 10
            issues.append(f"High HTTP request count ({requests_count})")
            services.add("Web Development")
        elif requests_count > 30:
            performance -= 5
            issues.append(f"HTTP requests need improvement ({requests_count})")
            services.add("Web Development")
        # Caching
        cache = r.headers.get("Cache-Control", "")
        server = r.headers.get("Server", "").lower()
        if not cache and "cloudflare" not in server:
            performance -= 5
            issues.append("Caching/CDN not detected")
            services.add("Web Development")

        # 2. RESPONSIVENESS

        viewport = soup.find("meta", attrs ={"name":re.compile("^viewport$",re.I)})
        if not viewport:
            mobile -= 30
            issues.append("Viewport meta tag missing")
            services.update(["Web Development" , "UI/UX"])
        # Check responsive CSS from HTML
        html_lower = r.text.lower()
        if "@media" not in html_lower:
            mobile -= 25
            issues.append("Responsive CSS not detected")
            services.update(["Web Development", "UI/UX"])
        # Fixed width detection
        fixed_width = re.search(r'width\s*=\s*["\'](?:[8-9]\d{2}|[1-9]\d{3,})',html_lower)
        if fixed_width:
            mobile -= 15
            issues.append("Potential horizontal scrolling issue")
            services.update(["Web Development","UI/UX"])

        # 3. SEO

        title = soup.title

        if not title or not title.get_text(strip=True):
            issues.append("Missing title tag")
            services.add("Digital Marketing")

        description = soup.find("meta",attrs={"name": re.compile("^description$", re.I)})

        if not description:
            issues.append("Missing meta description")
            services.add("Digital Marketing")

        h1 = soup.find_all("h1")

        if not h1:
            issues.append("H1 heading missing")
            services.add("Digital Marketing")

        elif len(h1) > 1:
            issues.append("Multiple H1 headings")
            services.add("Digital Marketing")

        # ALT text
        missing_alt = sum(
            not img.get("alt")
            for img in images)

        if missing_alt:
            issues.append(f"{missing_alt} image(s) missing ALT text")
            services.add("Digital Marketing")

        # Schema
        if not soup.find("script",type="application/ld+json"):
            issues.append("Schema markup not detected")
            services.add("Digital Marketing")

        # 4. UI / UX

        if not soup.find("nav"):
            issues.append("Navigation structure not detected")
            services.add("UI/UX")

        # 5. CODE QUALITY

        inline_styles = len(soup.select("[style]"))

        if inline_styles > 20:
            issues.append("Excessive inline styles")
            services.add("Web Development")

        # 6. SECURITY

        if not r.url.startswith("https://"):
            issues.append("HTTPS not enabled")
            services.add("Web Development")

        # 7. CONTENT

        text = soup.get_text(" ",strip=True)

        if len(text) < 300:
            issues.append("Limited website content")
            services.update(["Web Development","Digital Marketing"])

        # FINAL SCORES

        performance = max(0,min(100, performance))

        mobile = max(0,min(100, mobile))

        return {
            "Performance Score": performance,
            "Mobile Score": mobile,
            "Issues": issues,
            "Services": services
        }

    except Exception as e:

        print("Website analysis error:",e)

        return {
            "Performance Score": 0,
            "Mobile Score": 0,
            "Issues": ["Website could not be accessed"],
            "Services": {"Web Development"}
        }

# LEAD ANALYSIS

def analyze_websites(leads):

    if hasattr(leads, "to_dict"):
        leads = leads.to_dict("records")

    for lead in leads:

        company = lead.get("Lead Name", "")
        website = lead.get("Website", "")

        print(f"\nAnalyzing: {company}")

        # NO WEBSITE = HIGH OPPORTUNITY

        if not website:

            lead["Lead Score"] = 100
            lead["Priority"] = "Hot"
            lead["Recommended Services"] = ("Web Development, UI/UX")
            lead["Issues"] = "No website available"

            print("Lead Score: 100")
            print("Priority: Hot")

            continue

        # WEBSITE

        data = analyze_website(website)

        performance = data["Performance Score"]
        mobile = data["Mobile Score"]

        issues = data["Issues"]
        services = data["Services"]

        # LEAD SCORE
        # ==========================================

        performance_opportunity = 100 - performance
        mobile_opportunity = 100 - mobile

        issue_score = min(len(issues) * 10,100)

        lead_score = round( performance_opportunity * 0.35 + mobile_opportunity * 0.25 + issue_score * 0.40)
        # PRIORITY
        # ==========================================

        if lead_score >= 70:
            priority = "Hot"

        elif lead_score >= 40:
            priority = "Warm"

        else:
            priority = "Cold"

        # OUTPUT
        # ==========================================

        lead["Lead Score"] = lead_score
        lead["Priority"] = priority

        lead["Recommended Services"] = ", ".join(sorted(services))

        lead["Issues"] = ( "; ".join(issues)if issues else "No major issues detected")

        print( "Performance Score:",performance)

        print("Mobile Score:",mobile)

        print("Lead Score:",lead_score )

        print("Priority:",priority )

        print("Recommended Services:",lead["Recommended Services"])

        print("Issues:", lead["Issues"])

    return leads