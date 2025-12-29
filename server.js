const express = require('express');
const cors = require('cors');
const twilio = require('twilio');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Serve static files from current directory

// Twilio Configuration
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioWhatsAppNumber = process.env.TWILIO_WHATSAPP_NUMBER; // Format: whatsapp:+14155238886
const yourWhatsAppNumber = process.env.YOUR_WHATSAPP_NUMBER; // Format: whatsapp:+48123456789

const client = twilio(accountSid, authToken);

// Format message for WhatsApp
function formatWhatsAppMessage(data) {
    const { mode, estimatedPrice, contact, configuration } = data;
    
    let message = `🎬 *NOWE ZAPYTANIE - N STUDIOS*\n\n`;
    message += `*Tryb:* ${mode === 'traditional' ? 'TRADYCYJNE' : 'AI REKLAMA'}\n`;
    message += `*Szacowana cena:* ${estimatedPrice} PLN\n\n`;
    
    message += `👤 *Dane kontaktowe:*\n`;
    message += `Imię: ${contact.name}\n`;
    message += `Telefon: ${contact.phone}\n`;
    message += `Email: ${contact.email}\n\n`;
    
    message += `⚙️ *Konfiguracja:*\n`;
    
    if (mode === 'traditional') {
        message += `Sprzęt: ${configuration.equipment}\n`;
        message += `Studio: ${configuration.studio}\n`;
        message += `Długość: ${configuration.length}s\n`;
        message += `Złożoność: ${configuration.complexity}\n`;
    } else {
        message += `Długość: ${configuration.length}s\n`;
    }
    
    message += `\n⏰ Data: ${new Date(data.timestamp).toLocaleString('pl-PL')}`;
    
    return message;
}

// API endpoint to receive form submissions
app.post('/api/submit', async (req, res) => {
    try {
        const formData = req.body;
        
        // Validate required fields
        if (!formData.contact || !formData.contact.name || !formData.contact.phone || !formData.contact.email) {
            return res.status(400).json({ 
                success: false, 
                error: 'Brak wymaganych danych kontaktowych' 
            });
        }

        // Format message
        const message = formatWhatsAppMessage(formData);
        
        // Send WhatsApp message via Twilio
        const twilioMessage = await client.messages.create({
            body: message,
            from: twilioWhatsAppNumber,
            to: yourWhatsAppNumber
        });

        console.log('✓ WhatsApp notification sent successfully:', twilioMessage.sid);
        console.log('Form data:', JSON.stringify(formData, null, 2));

        res.json({ 
            success: true, 
            message: 'Zapytanie zostało wysłane pomyślnie',
            messageSid: twilioMessage.sid
        });

    } catch (error) {
        console.error('Error sending WhatsApp notification:', error);
        
        res.status(500).json({ 
            success: false, 
            error: 'Błąd podczas wysyłania zapytania',
            details: error.message 
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        message: 'Server is running',
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`
╔═══════════════════════════════════════════════╗
║   N STUDIOS - Backend Server                  ║
║   Port: ${PORT}                                   ║
║   Status: Running ✓                           ║
╚═══════════════════════════════════════════════╝
    `);
    
    // Check if Twilio credentials are configured
    if (!accountSid || !authToken) {
        console.warn('⚠️  WARNING: Twilio credentials not configured!');
        console.warn('   Please set up your .env file with Twilio credentials.');
    } else {
        console.log('✓ Twilio credentials loaded');
    }
});

module.exports = app;
