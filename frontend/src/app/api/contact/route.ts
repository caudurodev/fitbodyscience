import { NextResponse } from 'next/server';
import formData from 'form-data';
import Mailgun from 'mailgun.js';

const mailgun = new Mailgun(formData);
const DOMAIN = process.env.MAILGUN_DOMAIN || 'mg.curedigest.com';
const RECIPIENT_EMAIL = 'rod@cauduro.dev'; // Replace with your email address

const mg = mailgun.client({
    username: 'api',
    key: process.env.MAILGUN_API_KEY || 'key-yourkeyhere',
    url: 'https://api.eu.mailgun.net'
});

export async function POST(req: Request) {
    try {
        const { email, subject, message } = await req.json();

        if (!email || !subject || !message) {
            return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
        }

        const result = await mg.messages.create(DOMAIN, {
            from: `Contact Form <mailgun@mg.curedigest.com>`,
            to: RECIPIENT_EMAIL,
            subject: `FitBodyScience.com New contact form submission: ${subject}`,
            text: `Email: ${email}\nSubject: ${subject}\n\nMessage:\n${message}`,
            html: `<p><strong>Email:</strong> ${email}</p>
                   <p><strong>Subject:</strong> ${subject}</p>
                   <p><strong>Message:</strong></p>
                   <p>${message.replace(/\n/g, '<br>')}</p>`
        });

        console.log('Contact form submission sent successfully:', result);
        return NextResponse.json({ message: 'Message sent successfully' });

    } catch (error: any) {
        console.error('Error sending contact form submission:', error);

        if (error.status === 401) {
            return NextResponse.json({
                error: 'Authentication failed. Please check your Mailgun API key and domain.',
                details: error.message
            }, { status: 401 });
        }

        if (error.status === 403) {
            return NextResponse.json({
                error: 'Forbidden. Please check your Mailgun domain and API key.',
                details: error.message
            }, { status: 403 });
        }

        return NextResponse.json({ error: 'Failed to send email', details: error.message }, { status: 500 });
    }
}