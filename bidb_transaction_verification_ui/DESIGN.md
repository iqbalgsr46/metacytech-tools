---
name: Sovereign Heritage
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#53424b'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#85727b'
  outline-variant: '#d8c0cb'
  surface-tint: '#9c377b'
  primary: '#410030'
  on-primary: '#ffffff'
  primary-container: '#66004d'
  on-primary-container: '#e674bc'
  inverse-primary: '#ffaedc'
  secondary: '#7a590c'
  on-secondary: '#ffffff'
  secondary-container: '#fed17b'
  on-secondary-container: '#78580b'
  tertiary: '#002420'
  on-tertiary: '#ffffff'
  tertiary-container: '#003b35'
  on-tertiary-container: '#6ba79e'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd8eb'
  primary-fixed-dim: '#ffaedc'
  on-primary-fixed: '#3c002c'
  on-primary-fixed-variant: '#7f1d62'
  secondary-fixed: '#ffdea5'
  secondary-fixed-dim: '#ecc06c'
  on-secondary-fixed: '#271900'
  on-secondary-fixed-variant: '#5d4200'
  tertiary-fixed: '#b1eee4'
  tertiary-fixed-dim: '#95d2c8'
  on-tertiary-fixed: '#00201c'
  on-tertiary-fixed-variant: '#095049'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: IBM Plex Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

This design system is built on the pillars of **Trust, Heritage, and Modernity**. It serves a diverse banking demographic—from institutional investors to retail customers—requiring a UI that feels both authoritative and accessible. 

The aesthetic is **Corporate / Modern** with a subtle **Tactile** influence. It avoids the coldness of pure minimalism by using the brand's heritage colors (Purple and Gold) to create a warm, "white-glove" service atmosphere. The interface emphasizes security through structured layouts, high-contrast typography, and deliberate use of negative space to ensure clarity in financial decision-making.

The emotional response should be one of "Unshakable Security"—where every interaction feels intentional and every piece of data is presented with institutional precision.

## Colors

The palette is anchored by the BIBD Royal Purple and a refined Sovereign Gold.

*   **Primary (Purple):** Used for primary actions, navigation headers, and brand moments. It represents authority and stability.
*   **Secondary (Gold):** Used sparingly as an accent for "Premium" features, successful transaction states, and decorative heritage flourishes.
*   **Tertiary (Teal):** Derived from the BDCB logo context, used for financial growth indicators and secondary "safe" actions.
*   **Neutrals:** A sophisticated range of cool grays. Backgrounds stay off-white (`#F8F9FA`) to reduce eye strain while maintaining a clean, professional canvas.
*   **Status:** Standardized semantic colors for Error (Red), Warning (Amber), and Success (Green) are tuned to maintain accessibility against the primary purple.

## Typography

Typography is systematic and high-functioning. 

1.  **Manrope (Headlines):** Chosen for its modern, geometric construction that remains friendly yet professional. It provides the "modern banking" feel.
2.  **Inter (Body):** The industry standard for legibility. Used for all transactional data and long-form text to ensure no ambiguity in numbers or terms.
3.  **IBM Plex Sans (Labels/Data):** Its technical, slightly condensed nature makes it perfect for button labels, form headers, and tabular financial data where space is premium but clarity is mandatory.

**Scaling:** On mobile devices, large headlines scale down to prevent excessive wrapping. Maintain a minimum of 16px for body text to ensure accessibility for all age groups.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a strict 8px base unit rhythm.

*   **Desktop:** 12-column grid. Financial dashboards utilize the full width to display complex data, while informational pages are centered with a 1280px max-width.
*   **Mobile:** 4-column grid with generous 20px margins to prevent accidental taps near the bezel.
*   **Rhythm:** Vertical spacing between form elements (stacking) is kept tight (16px) to keep "related" information grouped, while section spacing is expansive (48px+) to allow the design to "breathe" and reduce cognitive load.

## Elevation & Depth

To convey security, depth is used sparingly and logically.

*   **Tonal Layers:** Use light-gray surface containers (`#F1F3F5`) to group related financial inputs against the main background.
*   **Ambient Shadows:** Primary cards (Account Summaries) use a very soft, multi-layered shadow: `0 4px 20px rgba(0,0,0,0.05)`. This creates a subtle "lift" without appearing "floaty."
*   **Active States:** When a user interacts with a secure input, the shadow should slightly deepen, and the border should transition to a 2px Primary Purple stroke to signal "Focus and Security."
*   **Overlays:** Modal windows for transaction confirmations use a 40% opacity blur backdrop to keep the user focused on the final "Confirm" action.

## Shapes

The design system utilizes **Soft** geometry. 

*   **Corner Radii:** A consistent 0.25rem (4px) or 0.5rem (8px) radius is used. This strikes a balance between the "sharpness" of traditional institutional banking and the "softness" of modern fintech. 
*   **Buttons:** Standard buttons use 4px corners to feel sturdy. Secondary "pills" or tags can use a full-round radius for better visual distinction in dense lists.
*   **Iconography:** Icons should have a consistent 1.5pt stroke weight with slightly rounded terminals to match the font characteristics of Manrope.

## Components

### Buttons
*   **Primary:** Solid Primary Purple (`#66004D`) with White text. High-contrast, no gradient.
*   **Secondary:** White background with a 1px Gold (`#C9A050`) border. Used for "Cancel" or "Go Back."
*   **Ghost:** Text-only in Primary Purple, used for tertiary navigation.

### Secure Input Fields
*   **Structure:** Label (IBM Plex Sans, Semi-bold), Input Area, and optional Helper Text.
*   **Visuals:** 1px border (`#DEE2E6`). On focus, the border becomes 2px Primary Purple.
*   **Password/PIN:** Must include a toggle for visibility and a strength meter using semantic colors.

### CAPTCHA Containers
*   Designed as a "Security Checkpoint." 
*   Encased in a light-teal tinted container (`#F0F7F6`) with a "Secure Link" icon. 
*   Action buttons within CAPTCHAs use the Tertiary Teal to distinguish them from main financial actions.

### Cards & Lists
*   **Account Cards:** Use a subtle Gold gradient header (top 4px) to signify "Premium/Active" status.
*   **Transaction Lists:** Alternate rows with a very faint gray to aid horizontal eye tracking across currency figures.

### Status Chips
*   Compact, semi-transparent backgrounds with high-saturation text (e.g., a light green background with dark green text for "Completed").