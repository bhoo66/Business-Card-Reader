import cv2
import pytesseract
import re
import pandas as pd
import imutils

# Set the path for Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load the image
image_path = "11.webp"
img = cv2.imread(image_path)
img = imutils.resize(img, width=500)
cv2.imshow(image_path, img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

text_image = pytesseract.image_to_string(img)
print(text_image)
text_lst = text_image.splitlines()  # This is to get each line as a separate text
text_lst = [word for word in text_lst if len(word) != 0]


def get_full_name(lst):
    for idx in lst:
        full_name = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", idx)
        if full_name is not None:
            return idx


def get_email(lst):
    for idx in lst:
        mail = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', idx)
        if mail is not None:
            return idx


def get_phone_number(lst):
    phone_patterns = [
        r'\+?\d[\d\s\-()]{7,}\d',
        r'\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}',
        r'\d{2,4}[\s\-]\d{2,4}[\s\-]\d{2,4}[\s\-]\d{2,4}',
        r'\d{10}'
    ]

    for idx in lst:
        for pattern in phone_patterns:
            match = re.search(pattern, idx)
            if match:
                return match.group(0)
    
    return None


def determine_card_type(lst):
    keywords = {
        'medical': ['medical', 'health', 'insurance', 'clinic'],
        'product': ['product', 'loyalty', 'points'],
        'retail': ['retail', 'shopping', 'store'],
        'IT Company':['job','it consultant'],
        'Institute':['institute','medical','school'],
        'Design Studio':['design','fashion']

    }

    for line in lst:
        for card_type, terms in keywords.items():
            for term in terms:
                if term in line.lower():
                    return card_type
    return 'Unknown'


def determine_card_purpose(lst):
    keywords = {
        'personal': ['personal', 'individual', 'private'],
        'Dental Clinic':['medical','clinic'],
        'life insurance': ['medical', 'health', 'insurance', 'asset'],
        'business': ['business', 'company', 'corporate'],
        'membership': ['membership', 'club', 'association'],
        'client needs':['job','it consultant'],
        'Market Designs':['grahic design','networking'],
        'Medical':['medicine']
    }

    for line in lst:
        for purpose, terms in keywords.items():
            for term in terms:
                if term in line.lower():
                    return purpose
    return 'Unknown'


# Extracting information
final_text = {
    "Name": get_full_name(text_lst),
    "Telephone": get_phone_number(text_lst),
    "Email": get_email(text_lst),
    "CardType": determine_card_type(text_lst),
    "CardPurpose": determine_card_purpose(text_lst)
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame([final_text])

# Save the DataFrame to a CSV file
excel_path = 'data.csv'
df.to_csv(excel_path, index=False)

print(f"Details extracted and saved to {excel_path}")
print(final_text)

cv2.waitKey(0)
