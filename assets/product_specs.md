# Product Specifications: E-Shop Checkout

## Overview
The E-Shop Checkout page is the final step for users to purchase items. It allows users to enter shipping details, select shipping and payment methods, apply discounts, and complete the purchase.

## Features

### 1. User Details Form
- **Fields**:
    - Full Name (Text, Required)
    - Email (Email, Required, must contain '@')
    - Address (Text, Required)
- **Validation**:
    - If any required field is empty, show an inline error message in red.
    - If email is invalid, show "Please enter a valid email".

### 2. Shipping Methods
- **Standard Shipping**:
    - Cost: Free ($0.00)
    - Default selection.
- **Express Shipping**:
    - Cost: $10.00 added to the total.

### 3. Payment Methods
- **Credit Card**: Default selection.
- **PayPal**: Option available.

### 4. Discount Code
- Users can enter a discount code.
- **Code: SAVE15**:
    - Applies a 15% discount to the *item subtotal* (before shipping).
    - Success message: "15% Discount Applied!" (Green text).
- **Invalid Code**:
    - Error message: "Invalid Code" (Red text).

### 5. Cart Summary
- Displays list of items.
- Displays Total Price.
- Total Price = (Item Subtotal * Discount Multiplier) + Shipping Cost.
- Initial Total: $248.00 (Headphones $99 + Watch $149).

### 6. Pay Now
- Button labeled "Pay Now".
- Color: Green (#4CAF50).
- On Click:
    - Validate form.
    - If valid: Hide form, display "Payment Successful!" (Green text).
    - If invalid: Show error messages.
