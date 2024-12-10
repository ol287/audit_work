import re

def mask_name(name):
    """
    Masks a name, revealing only the first letter and replacing the rest with '*'.
    """
    parts = name.split()
    masked_parts = [p[0] + '*' * (len(p) - 1) for p in parts]
    return ' '.join(masked_parts)

def mask_email(email):
    """
    Masks an email address, showing the first letter of the local part, the domain's first letter,
    and hiding the rest with '*'.
    """
    local, domain = email.split('@')
    domain_name, domain_extension = domain.split('.')
    masked_local = local[0] + '*' * (len(local) - 1)
    masked_domain_name = domain_name[0] + '*' * (len(domain_name) - 1)
    return f"{masked_local}@{masked_domain_name}.{domain_extension}"

def mask_phone(phone):
    """
    Masks a phone number, showing the last four digits and masking the rest with '*'.
    Supports multiple phone formats.
    """
    digits = re.sub(r'\D', '', phone)  # Remove all non-digit characters
    return '*' * (len(digits) - 4) + digits[-4:]

def mask_sensitive_data(data, fields_to_mask):
    """
    Masks sensitive fields in a dataset.
    
    :param data: List of dictionaries containing the dataset.
    :param fields_to_mask: List of fields to mask.
    :return: Dataset with masked sensitive fields.
    """
    masked_data = []
    for record in data:
        masked_record = record.copy()
        for field in fields_to_mask:
            if field in masked_record:
                value = masked_record[field]
                if field == 'name':
                    masked_record[field] = mask_name(value)
                elif field == 'email':
                    masked_record[field] = mask_email(value)
                elif field == 'phone':
                    masked_record[field] = mask_phone(value)
                else:
                    masked_record[field] = '*' * len(str(value))  # Generic masking
        masked_data.append(masked_record)
    return masked_data

# Sample dataset
data = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "phone": "(123) 456-7890"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com", "phone": "987-654-3210"}
]

# Fields to mask
fields_to_mask = ["name", "email", "phone"]

# Mask sensitive information
masked_data = mask_sensitive_data(data, fields_to_mask)

# Print results
for original, masked in zip(data, masked_data):
    print("Original:", original)
    print("Masked:  ", masked)
    print()
