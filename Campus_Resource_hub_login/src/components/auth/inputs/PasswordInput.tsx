/**
 * @component PasswordInput (cmp/input/password)
 * @description Enterprise-grade password input with strength indicator
 */

import { Input } from "../../ui/input";
import { Label } from "../../ui/label";
import { Eye, EyeOff } from "lucide-react";
import { useState, useEffect } from "react";

interface PasswordInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  label?: string;
  placeholder?: string;
  required?: boolean;
  showStrength?: boolean;
}

export function PasswordInput({ 
  value, 
  onChange, 
  disabled = false,
  label = "Password",
  placeholder = "Enter password",
  required = false,
  showStrength = false
}: PasswordInputProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [strength, setStrength] = useState(0);
  const [touched, setTouched] = useState(false);
  
  useEffect(() => {
    if (!value) {
      setStrength(0);
      return;
    }
    
    let score = 0;
    if (value.length >= 8) score++;
    if (value.length >= 12) score++;
    if (/[A-Z]/.test(value)) score++;
    if (/[0-9]/.test(value)) score++;
    if (/[^A-Za-z0-9]/.test(value)) score++;
    
    setStrength(Math.min(score, 4));
  }, [value]);
  
  const strengthColors = ['', '#ef5350', '#ff9800', '#ffc107', '#43a047'];
  const strengthLabels = ['', 'Weak', 'Fair', 'Good', 'Strong'];

  return (
    <div className="group" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Label 
          htmlFor="password" 
          style={{ 
            fontSize: 'var(--text-base)', 
            color: 'var(--color-text-primary)',
            fontWeight: 500,
            letterSpacing: 'var(--letter-spacing-normal)'
          }}
        >
          {label}
          {required && <span style={{ color: 'var(--color-error)', marginLeft: 'var(--space-1)' }}>*</span>}
        </Label>
        {showStrength && touched && value && (
          <span 
            style={{ 
              fontSize: 'var(--text-sm)', 
              color: strengthColors[strength],
              fontWeight: 500,
              animation: 'fadeIn var(--transition-base)'
            }}
          >
            {strengthLabels[strength]}
          </span>
        )}
      </div>
      <div className="relative">
        <Input 
          id="password" 
          type={showPassword ? "text" : "password"}
          placeholder={placeholder}
          value={value}
          onChange={(e) => {
            onChange(e.target.value);
            if (!touched) setTouched(true);
          }}
          disabled={disabled}
          className="input-glow transition-all"
          style={{
            height: 'var(--input-height)',
            borderRadius: 'var(--radius-md)',
            fontSize: 'var(--text-md)',
            paddingRight: 'var(--space-10)',
            borderColor: 'var(--color-border-default)',
            backgroundColor: 'var(--color-bg-default)',
            boxShadow: 'var(--shadow-xs)'
          }}
          onBlur={() => setTouched(true)}
          onFocus={(e) => {
            e.target.style.boxShadow = '0 0 0 3px var(--focus-ring-color), var(--shadow-sm)';
            e.target.style.borderColor = 'var(--iu-crimson)';
          }}
          onBlurCapture={(e) => {
            e.target.style.boxShadow = 'var(--shadow-xs)';
            e.target.style.borderColor = 'var(--color-border-default)';
          }}
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          disabled={disabled}
          className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors"
          style={{
            color: 'var(--color-text-secondary)',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-text-primary)'}
          onMouseLeave={(e) => e.currentTarget.style.color = 'var(--color-text-secondary)'}
        >
          {showPassword ? (
            <EyeOff className="size-5" />
          ) : (
            <Eye className="size-5" />
          )}
        </button>
      </div>
      {showStrength && touched && value && (
        <div style={{ display: 'flex', gap: 'var(--space-1)', animation: 'slideDown var(--transition-base)' }}>
          {[1, 2, 3, 4].map((level) => (
            <div
              key={level}
              style={{
                flex: 1,
                height: '3px',
                borderRadius: 'var(--radius-full)',
                backgroundColor: strength >= level ? strengthColors[strength] : 'var(--color-border-default)',
                transition: 'all var(--transition-base)'
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}
