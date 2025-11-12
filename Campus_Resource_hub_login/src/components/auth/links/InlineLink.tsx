/**
 * @component InlineLink (cmp/link/inline)
 * @description Enterprise-grade text link with smooth animations
 */

import { AnchorHTMLAttributes } from "react";

interface InlineLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  variant?: "primary" | "secondary";
  children: React.ReactNode;
}

export function InlineLink({ 
  variant = "primary", 
  children, 
  className = "",
  ...props 
}: InlineLinkProps) {
  const colorPrimary = "var(--iu-crimson)";
  const colorSecondary = "var(--color-text-secondary)";
  const color = variant === "primary" ? colorPrimary : colorSecondary;
  
  return (
    <a 
      {...props}
      className={`hover:underline ${className}`}
      style={{ 
        fontSize: 'var(--text-base)', 
        color: color,
        fontWeight: 500,
        cursor: 'pointer',
        transition: 'color var(--transition-fast)',
        textDecoration: 'none'
      }}
      onMouseEnter={(e) => {
        if (variant === "primary") {
          e.currentTarget.style.color = "var(--iu-crimson-dark)";
        } else {
          e.currentTarget.style.color = "var(--color-text-primary)";
        }
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.color = color;
      }}
    >
      {children}
    </a>
  );
}
