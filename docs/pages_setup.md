# Virtual Cavity RF Simulator - Documentation Site

This directory contains the configuration for automatically generating the project's GitHub Pages website.

## 🌐 Website Features

The generated website includes:

- **Professional Landing Page**: Modern, responsive design with Bootstrap
- **Feature Showcase**: Interactive cards highlighting key capabilities  
- **Installation Guide**: Step-by-step setup instructions
- **Usage Examples**: Code snippets and demonstrations
- **Technical Specifications**: Detailed parameter documentation
- **API Reference**: Complete documentation links

## 🔧 Automatic Generation

The website is automatically built and deployed using GitHub Actions:

1. **Trigger**: Pushes to main branch or manual workflow dispatch
2. **Build Process**: 
   - Converts README.md to HTML documentation
   - Generates professional landing page
   - Processes all markdown files
   - Optimizes for mobile and desktop
3. **Deployment**: Publishes to GitHub Pages

## 📱 Responsive Design

The website features:
- Bootstrap 5 responsive framework
- Mobile-first design approach
- Professional color scheme
- Interactive navigation
- Syntax highlighting for code blocks

## 🎨 Customization

To customize the website:

1. Edit `.github/workflows/pages.yml` for build configuration
2. Modify the HTML template in the Python generation script
3. Add new pages by extending the build process
4. Update styling in the embedded CSS

## 🚀 Access Your Website

Once deployed, your website will be available at:
**https://iuming.github.io/virtual-cavity-simulator/**

## 📊 Analytics and SEO

The website includes:
- Meta tags for search engine optimization
- Open Graph tags for social media sharing
- Responsive viewport configuration
- Semantic HTML structure
- Fast loading with CDN resources

## 🔄 Updates

The website automatically updates when you:
- Push changes to the main branch
- Update README.md or documentation
- Modify the workflow configuration
- Manually trigger the workflow

This ensures your project website stays current with your latest development.
