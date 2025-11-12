/**
 * @component FormFeedbackAlert (cmp/alert/form-feedback)
 * @description Enterprise-grade contextual alert banners
 */

import { AlertCircle, CheckCircle, Info, X } from "lucide-react";
import { useState } from "react";

interface FormFeedbackAlertProps {
  variant: "error" | "success" | "info" | "warning";
  children: React.ReactNode;
  dismissible?: boolean;
  onDismiss?: () => void;
}

export function FormFeedbackAlert({ 
  variant, 
  children, 
  dismissible = false,
  onDismiss 
}: FormFeedbackAlertProps) {
  const [isVisible, setIsVisible] = useState(true);
  
  const styles = {
    error: {
      borderColor: "var(--color-error)",
      iconColor: "var(--iu-crimson)",
      textColor: "var(--color-error)",
      bgColor: "var(--color-bg-error)",
      Icon: AlertCircle,
    },
    success: {
      borderColor: "var(--color-success)",
      iconColor: "var(--color-success)",
      textColor: "var(--color-success)",
      bgColor: "var(--color-bg-success)",
      Icon: CheckCircle,
    },
    info: {
      borderColor: "var(--color-info-light)",
      iconColor: "var(--color-info-light)",
      textColor: "var(--color-info)",
      bgColor: "var(--color-bg-info)",
      Icon: Info,
    },
    warning: {
      borderColor: "#f57c00",
      iconColor: "#f57c00",
      textColor: "#e65100",
      bgColor: "#fff3e0",
      Icon: AlertCircle,
    },
  };

  const config = styles[variant];
  const IconComponent = config.Icon;
  
  const handleDismiss = () => {
    setIsVisible(false);
    onDismiss?.();
  };
  
  if (!isVisible) return null;

  return (
    <div
      className="flex items-start gap-3"
      style={{
        backgroundColor: config.bgColor,
        borderLeft: `3px solid ${config.borderColor}`,
        borderRadius: 'var(--radius-sm)',
        padding: 'var(--space-3)',
        boxShadow: 'var(--shadow-xs)',
        animation: 'slideDown var(--transition-base)'
      }}
    >
      <IconComponent
        className="size-5 shrink-0"
        style={{ 
          color: config.iconColor, 
          marginTop: '1px'
        }}
      />
      <div
        className="flex-1"
        style={{
          color: config.textColor,
          fontSize: "var(--text-base)",
          lineHeight: "var(--line-height-relaxed)",
        }}
      >
        {children}
      </div>
      {dismissible && (
        <button
          onClick={handleDismiss}
          className="shrink-0 transition-colors"
          style={{
            color: config.textColor,
            opacity: 0.6,
            cursor: 'pointer',
            background: 'none',
            border: 'none',
            padding: 0
          }}
          onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
          onMouseLeave={(e) => e.currentTarget.style.opacity = '0.6'}
        >
          <X className="size-4" />
        </button>
      )}
    </div>
  );
}
