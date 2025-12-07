import pandas as pd
import numpy as np
import random

def generate_dummy_data(n_samples=200):
    """
    Generates a synthetic dataset of emails for training.
    """
    phishing_templates = [
        "Urgent: Verify your account immediately at {url}",
        "You have won a lottery! Click here {url} to claim.",
        "Security Alert: Unusual sign-in activity detected. Visit {url}",
        "Your bank account has been suspended. Restore access: {url}",
        "Dear user, your password expires in 24 hours. Update now: {url}",
        "Payment overdue. Pay now to avoid legal action. {url}",
        "Exclusive offer just for you! 90% off. {url}",
        "Verify your identity to keep using our services. {url}",
        "Action required: Confirm your email address. {url}"
    ]
    
    safe_templates = [
        "Meeting reminder for tomorrow at 10 AM.",
        "Here are the project files you requested.",
        "Happy Birthday! Hope you have a great day.",
        "Invoice for your recent purchase is attached.",
        "Let's catch up for lunch this week.",
        "The weekly newsletter is out. Check it out.",
        "Your package has been delivered.",
        "Team outing details. Please RSVP.",
        "Agenda for the upcoming board meeting."
    ]
    
    urls = [
        "http://suspicious-site.com/login",
        "http://secure-bank-verify.net",
        "http://account-update.info",
        "http://lottery-winner.xyz"
    ]
    
    safe_urls = [
        "https://google.com",
        "https://linkedin.com",
        "https://github.com",
        "https://medium.com"
    ]
    
    data = []
    
    for _ in range(n_samples // 2):
        # Generate Phishing Email
        template = random.choice(phishing_templates)
        url = random.choice(urls)
        body = template.format(url=url)
        data.append({"body": body, "label": 1}) # 1 for phishing
        
        # Generate Safe Email
        template = random.choice(safe_templates)
        # Occasionally add a safe URL to safe emails
        if random.random() > 0.7:
             body = template + " " + random.choice(safe_urls)
        else:
             body = template
        data.append({"body": body, "label": 0}) # 0 for safe
        
    df = pd.DataFrame(data)
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    return df

def load_data(filepath=None):
    if filepath:
        return pd.read_csv(filepath)
    else:
        return generate_dummy_data()
