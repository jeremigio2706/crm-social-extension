# CRM Social Extension

A comprehensive Odoo module that enhances CRM functionality with social media integration and customer promotion features.

## Features

### 🔗 Social Media Integration

- **Customer Social Profiles**: Register Facebook, LinkedIn, and Twitter URLs for each customer
- **Visual Indicators**: See profile completion status across all customer views
- **URL Validation**: Automatic validation of social media URL formats
- **Profile Completion Tracking**: Real-time calculation of profile completion percentage

### 📊 Profile Management

- **Complete Profile Detection**: Automatic identification of customers with all social media profiles
- **Completion Rate Calculation**: Percentage-based tracking of profile completeness
- **Visual Status Indicators**: Badges and icons showing profile status in all views
- **Advanced Filtering**: Filter customers by profile completion status

### 🌐 Customer Promotion Website

- **Public Customer Directory**: Dedicated webpage showcasing customers with social media
- **Advanced Search**: Search by customer name, social media accounts, and website
- **Responsive Design**: Mobile-friendly interface with modern styling
- **Live Search**: Real-time search suggestions with AJAX
- **Customer Details**: Individual customer pages with complete social media integration

### 🎯 CRM Enhancement

- **Tab Integration**: New "Social Media" tab in customer forms
- **Kanban Cards**: Social media icons and completion status in kanban view
- **List View Columns**: Profile completion information in list views
- **Lead Integration**: Social profile status in CRM leads and opportunities

## Installation

1. Copy the module to your Odoo addons directory
2. Update the addons list: `Settings > Apps > Update Apps List`
3. Install the module: Search for "CRM Social Extension" and click Install

## Usage

### Adding Social Media URLs

1. Go to `Contacts` or `CRM > Customers`
2. Open a customer record
3. Navigate to the "Social Media" tab
4. Enter the social media URLs:
   - Facebook: <https://facebook.com/username>
   - LinkedIn: <https://linkedin.com/in/username> or /company/companyname
   - Twitter: <https://twitter.com/username>

### Viewing Customer Promotion Page

1. Navigate to your website
2. Click on "Our Customers" in the main menu
3. Browse customers with social media profiles
4. Use the search functionality to find specific customers
5. Click on individual customers for detailed views

### Filtering Customers

In the CRM or Contacts app:

- Use "Profile Complete" filter to see customers with all social media URLs
- Use "Profile Incomplete" filter to see customers missing some social media URLs
- Use "Has Social Media" filter to see all customers with at least one social media URL

## Technical Details

### Models Extended

- `res.partner`: Added social media fields and computed fields for profile completion

### New Fields

- `facebook_url`: Character field for Facebook URL
- `linkedin_url`: Character field for LinkedIn URL  
- `twitter_url`: Character field for Twitter URL
- `social_profile_complete`: Boolean computed field
- `social_profile_completion_rate`: Float computed field (percentage)

### Controllers

- `/customers`: Main customer promotion page
- `/customers/<id>`: Individual customer detail page
- `/customers/search`: AJAX search endpoint
- `/customers/stats`: Statistics API endpoint

### Views Enhanced

- Partner form view: Added Social Media tab
- Partner tree view: Added completion columns
- Partner kanban view: Added social indicators
- Partner search view: Added social media filters
- CRM lead form: Added social profile status

## Testing

The module includes comprehensive unit tests covering:

### Model Tests (`test_res_partner.py`)

- Social profile completion calculation
- URL validation for all platforms
- Search functionality
- Profile completion rate calculation
- Edge cases and validation scenarios

### Controller Tests (`test_customer_promotion_controller.py`)

- Website page accessibility
- Search functionality
- Customer detail pages
- AJAX endpoints
- Pagination
- Statistics calculation

### Running Tests

```bash
# Run all tests for the module
python odoo-bin -d test_db -i crm_social_extension --test-enable

# Run specific test file
python odoo-bin -d test_db --test-file=addons/crm_social_extension/tests/test_res_partner.py

# Run with coverage
python -m coverage run odoo-bin -d test_db -i crm_social_extension --test-enable
python -m coverage report
python -m coverage html
```

## Git Workflow

This project follows Git best practices:

### Branch Structure

- `main`: Production-ready code
- `develop`: Development integration branch
- `feature/*`: Feature development branches
- `hotfix/*`: Critical bug fixes

### Commit Messages

Following conventional commits format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `style:` Code formatting
- `refactor:` Code refactoring
- `test:` Test additions/modifications
- `chore:` Maintenance tasks

### Example Workflow

```bash
# Create feature branch
git checkout -b feature/social-media-validation

# Make changes and commit
git add .
git commit -m "feat: add URL validation for social media fields"

# Push and create pull request
git push origin feature/social-media-validation
```

## Configuration

### URL Validation Patterns

The module validates URLs using regex patterns:

- **Facebook**: `^https?://(www\.)?(facebook\.com|fb\.com)/.+`
- **LinkedIn**: `^https?://(www\.)?linkedin\.com/.+`
- **Twitter**: `^https?://(www\.)?(twitter\.com|x\.com)/.+`

### Customization

You can customize the social media platforms by modifying:

1. `models/res_partner.py`: Add new URL fields
2. `views/res_partner_views.xml`: Add new form fields
3. Update validation methods and social media data

## Performance Considerations

### Database Indexes

The module automatically creates indexes on:

- `social_profile_complete` field for filtering
- Social media URL fields for search performance

### Caching

- Social media data is computed and stored for performance
- Website pages use appropriate caching headers
- AJAX search includes debouncing to reduce server load

## Security

### Access Rights

- All social media fields respect existing partner access rights
- Website pages are public but only show company contacts
- No sensitive information is exposed in public views

### Data Validation

- URL validation prevents XSS attacks
- Input sanitization on all user inputs
- Proper escaping in website templates

## Compatibility

### Odoo Versions

- ✅ Odoo 13.0+
- ✅ Odoo 14.0+
- ✅ Odoo 15.0+
- ✅ Odoo 16.0+
- ✅ Odoo 17.0+
- ✅ Odoo 18.0+

### Dependencies

- `base`: Core Odoo functionality
- `crm`: CRM module
- `website`: Website builder
- `contacts`: Contact management

### Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Quality

- Follow Odoo coding guidelines
- Maintain test coverage above 80%
- Use proper docstrings
- Follow PEP 8 for Python code

## License

This module is licensed under AGPL-3.0. See LICENSE file for details.

## Support

For support and questions:

1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Contact the development team

## Changelog

### Version 18.0.1.0.0

- ✨ Initial release
- ✨ Social media URL fields for customers
- ✨ Profile completion tracking
- ✨ Customer promotion website
- ✨ Advanced search functionality
- ✨ Comprehensive test suite
- ✨ Modern responsive design
- ✨ AJAX-powered search
- ✨ Multi-platform URL validation
