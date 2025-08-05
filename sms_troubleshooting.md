# SMS Troubleshooting Guide

## Common Issues and Solutions

### 1. **Message says "sent successfully" but no SMS received**

This usually happens due to one of these reasons:

#### A. **Twilio Account Verification** (Most Common)
- **Trial accounts** require phone number verification
- Go to [Twilio Console](https://console.twilio.com/)
- Navigate to Phone Numbers → Manage → Verified Caller IDs
- Add and verify your phone number

#### B. **Phone Number Format**
- Ensure your phone number includes country code
- Correct format: `+919876543210` (for India)
- Avoid spaces or special characters

#### C. **Account Credits**
- Check if your Twilio account has sufficient credits
- Trial accounts get $15 USD in credits
- Check balance in Twilio Console → Dashboard

### 2. **Error Messages and Solutions**

#### "The number [number] is unverified"
- **Solution**: Verify your phone number in Twilio Console
- Go to Phone Numbers → Manage → Verified Caller IDs
- Click "Add a new number" and verify via SMS/call

#### "Invalid 'To' phone number"
- **Solution**: Check phone number format
- Must include country code: `+91` for India
- Remove any spaces or special characters

#### "Insufficient credits"
- **Solution**: Add credits to your Twilio account
- Or upgrade from trial to paid account

### 3. **Testing Your SMS Setup**

1. **Run the test script**:
   ```bash
   python test_sms.py
   ```

2. **Check Twilio Console**:
   - Go to Console → Monitor → Logs → Messaging
   - Look for your message attempts
   - Check error codes if any

3. **Manual verification**:
   ```python
   from twilio.rest import Client
   
   client = Client("your_account_sid", "your_auth_token")
   
   # Check account info
   account = client.api.accounts(client.account_sid).fetch()
   print(f"Account Status: {account.status}")
   
   # List verified numbers (for trial accounts)
   verified_numbers = client.validation_requests.list()
   print("Verified numbers:", [num.phone_number for num in verified_numbers])
   ```

### 4. **Verification Checklist**

Before testing SMS, ensure:

- [ ] Your phone number is verified in Twilio Console
- [ ] Phone number format includes country code (+91...)
- [ ] Twilio account has credits (check Dashboard)
- [ ] Account SID and Auth Token are correct
- [ ] Twilio phone number is active

### 5. **Alternative Testing Methods**

If SMS still doesn't work, try:

1. **WhatsApp instead of SMS**:
   - Use WhatsApp endpoint: `/whatsapp`
   - Format: `whatsapp:+919876543210`

2. **Use Twilio Studio**:
   - Create a simple flow in Twilio Studio
   - Test with your verified number

3. **Check regional restrictions**:
   - Some countries have SMS restrictions
   - Check Twilio's country-specific guidelines

### 6. **Debug Mode**

The updated SMS function now provides detailed information:
- Message SID
- Message Status
- From/To numbers
- Error messages (if any)

Monitor these details when testing.

### 7. **Support Resources**

- [Twilio SMS Documentation](https://www.twilio.com/docs/sms)
- [Twilio Console](https://console.twilio.com/)
- [Twilio Support](https://support.twilio.com/)

---

**Quick Fix**: Most SMS issues are resolved by verifying your phone number in the Twilio Console under "Verified Caller IDs".
