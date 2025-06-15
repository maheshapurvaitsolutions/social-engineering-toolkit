# Social Engineering Toolkit (SET)

A comprehensive security awareness training platform designed to help organizations train employees against social engineering attacks.

## Features

### 🎯 Simulated Social Engineering Attacks
- **Email Phishing Simulations**: Create realistic phishing email campaigns
- **Voice Phishing (Vishing)**: Phone-based social engineering tests
- **SMS Phishing (Smishing)**: Text message-based attacks
- **Physical Security Tests**: USB drop attacks and tailgating simulations

### 📚 Training Modules
- Interactive learning content
- Phishing awareness training
- Password security best practices
- Social engineering defense techniques
- Quizzes and assessments
- Progress tracking

### 📊 Reporting and Analytics
- Campaign performance metrics
- Training completion rates
- Employee vulnerability assessments
- Security posture dashboards
- Detailed analytics and insights

### 👥 User Management
- Role-based access control (Admin/User)
- Department-based organization
- Individual progress tracking
- Secure authentication

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone or extract the toolkit**:
   ```bash
   cd social-engineering-toolkit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the setup script**:
   ```bash
   python setup.py
   ```

4. **Start the application**:
   ```bash
   cd src
   python app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Demo Accounts

The setup script creates the following demo accounts:

- **Administrator**: 
  - Email: `admin@company.com`
  - Password: `admin123`
  - Access: Full administrative privileges

- **Regular User**:
  - Email: `user@company.com`
  - Password: `user123`
  - Access: Training modules and personal dashboard

## Usage

### For Administrators

1. **Login** with admin credentials
2. **Create Campaigns**:
   - Navigate to Campaigns → New Campaign
   - Choose campaign type (phishing, vishing, etc.)
   - Select target users
   - Configure templates and settings
3. **Monitor Results**:
   - View campaign performance in Reports
   - Track employee click rates and responses
   - Generate detailed reports
4. **Manage Training**:
   - Create custom training modules
   - Assign training to users
   - Monitor completion rates

### For Users

1. **Login** with user credentials
2. **Complete Training**:
   - Access assigned training modules
   - Take interactive quizzes
   - Track your progress
3. **View Dashboard**:
   - See security tips and best practices
   - Monitor your training status
   - Access security resources

## Security Features

### Educational Focus
- All simulations are clearly marked as training exercises
- Immediate educational feedback for clicked links
- No actual malicious code or data collection
- Safe, controlled environment for learning

### Data Protection
- Local SQLite database (no external dependencies)
- Password hashing using Werkzeug security
- Session-based authentication
- Input validation and sanitization

### Compliance
- Designed for educational purposes only
- Follows responsible disclosure practices
- Includes clear labeling of simulated attacks
- Provides immediate training feedback

## Technical Architecture

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Authentication**: Session-based with password hashing
- **Security**: Input validation, CSRF protection

### Frontend
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS with modern ES6 features
- **Styling**: Custom CSS with responsive design

### Database Schema
- Users and authentication
- Campaign management
- Training modules and progress
- Results and analytics

## Customization

### Adding Training Modules
1. Access the admin dashboard
2. Navigate to training management
3. Create new modules with custom content
4. Include interactive elements and quizzes

### Creating Campaign Templates
1. Edit email templates in the campaigns section
2. Customize phishing scenarios
3. Add company-specific branding and context

### Modifying the Interface
1. Edit HTML templates in `templates/`
2. Modify CSS styles in `static/css/style.css`
3. Add JavaScript functionality in `static/js/main.js`

## Best Practices

### Campaign Planning
- Start with awareness training before simulations
- Gradually increase complexity of attacks
- Provide immediate feedback and training
- Regular follow-up training sessions

### Employee Communication
- Announce the security awareness program
- Explain the educational purpose
- Provide support channels for questions
- Celebrate improvements and learning

### Continuous Improvement
- Regularly update attack scenarios
- Monitor industry trends and threats
- Adapt training based on results
- Seek employee feedback

## Troubleshooting

### Common Issues

**Database Connection Errors**:
- Ensure the `data/` directory exists
- Run `python setup.py` to recreate database
- Check file permissions

**Login Issues**:
- Verify demo account credentials
- Clear browser cookies and session data
- Restart the application

**Email Simulation Not Working**:
- Check SMTP configuration (if using real emails)
- For demo mode, campaigns are simulated only
- Verify target email addresses format

### Support
This is an educational toolkit. For production deployments:
- Review security configurations
- Implement proper logging and monitoring
- Consider professional security tools integration
- Ensure compliance with organizational policies

## Educational Disclaimer

This toolkit is designed for educational and authorized testing purposes only. Users must:
- Obtain proper authorization before conducting any simulations
- Use only within their own organization or with explicit permission
- Follow all applicable laws and regulations
- Provide appropriate training and support to participants

## Contributing

This is an educational project. Improvements and educational enhancements are welcome:
- Add new training modules
- Improve user interface
- Enhance reporting capabilities
- Add integration options

## License

This project is intended for educational use. Please ensure compliance with your organization's policies and applicable laws when using this toolkit.

---

**Remember**: The goal is education and awareness, not to trick or embarrass employees. Always provide constructive feedback and learning opportunities.

