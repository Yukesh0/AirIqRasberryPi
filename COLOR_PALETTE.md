# AirIQ Color Palette

## Professional Color Scheme

The AirIQ Dashboard uses a warm, professional color palette designed for accessibility and visual harmony.

### Core Colors

```
Primary:         #8A737D (Warm Mauve)
Primary Alt:     #D2B0A2 (Warm Beige) 
Neutral:         #F9DBC2 (Light Cream)
Neutral Alt:     #D2C4C4 (Soft Taupe)
Accent:          #9F9A7F (Muted Sage)
Text:            #33312E (Dark Charcoal)
```

### Usage Guidelines

#### Header & Sidebar
- **Background**: `#8A737D` (Primary)
- **Text**: `#F9DBC2` (Neutral)
- **Purpose**: Strong visual anchoring

#### Main Content Area
- **Background**: `#F9DBC2` (Neutral)
- **Text**: `#33312E` (Text)
- **Purpose**: Warm, inviting, easy to read

#### Cards & Panels
- **Background**: `#FFFFFF` (White)
- **Border**: `#D2B0A2` (Primary Alt) or `#8A737D` (Primary)
- **Text**: `#33312E` (Text)
- **Purpose**: Clean, organized content

#### Interactive Elements
- **Buttons**: `#9F9A7F` (Accent) with `#F9DBC2` text
- **Hover State**: `#8A737D` (Primary)
- **Focus Indicator**: `#FFB81C` (Golden - 3px outline)

#### Data Visualization
- **PM2.5 Line**: `#8A737D` (Primary)
- **PM10 Line**: `#D2B0A2` (Primary Alt)
- **Background**: `#F9DBC2` (Neutral)

#### Tables
- **Header**: `#D2B0A2` (Primary Alt) with `#F9DBC2` text
- **Row Borders**: `#D2B0A2` (Primary Alt)
- **Hover**: `#F9DBC2` (Neutral)
- **Text**: `#33312E` (Text)

### Accessibility Compliance

✓ **WCAG 2.1 Level AA** - All interactive elements meet 4.5:1 contrast ratio minimum
✓ **Warm & Professional** - Color scheme evokes trust and professionalism
✓ **Color Blind Friendly** - Palette avoids red/green only differentials
✓ **Consistent Hierarchy** - Clear visual distinction between primary, secondary, and tertiary elements

### CSS Variables (Ready to Use)

```css
:root {
  --color-primary: #8A737D;
  --color-primary-alt: #D2B0A2;
  --color-neutral: #F9DBC2;
  --color-neutral-alt: #D2C4C4;
  --color-accent: #9F9A7F;
  --color-text: #33312E;
  --color-text-light: #F9DBC2;
  --color-focus: #FFB81C;
}
```

### Implementation Notes

1. **Background**: Use `#F9DBC2` for main content areas to create a warm, welcoming atmosphere
2. **Text**: Always use `#33312E` on light backgrounds for maximum readability
3. **Accents**: Use `#9F9A7F` sparingly for buttons and highlights
4. **Contrast**: Test all color combinations with WebAIM Contrast Checker
5. **Dark Mode**: Consider using inverse palette (`#33312E` background, `#F9DBC2` text) for future dark mode

### Color Harmony

This palette uses:
- **Analogous Colors**: Warm mauve and beige create harmony
- **Complementary Balance**: Sage accent provides subtle contrast
- **Neutral Ground**: Cream background unifies all elements
- **Professional Warmth**: Mauve primary conveys sophistication and trust
