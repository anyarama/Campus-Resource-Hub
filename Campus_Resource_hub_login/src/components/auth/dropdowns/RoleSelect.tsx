/**
 * @component RoleSelect (cmp/dropdown/role-select)
 * @description Enterprise-grade role selection dropdown
 */

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../ui/select";
import { Label } from "../../ui/label";
import { Users } from "lucide-react";

interface RoleSelectProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  label?: string;
  required?: boolean;
}

export function RoleSelect({ 
  value, 
  onChange, 
  disabled = false,
  label = "I am a...",
  required = false
}: RoleSelectProps) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
      <Label 
        htmlFor="role" 
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
      <Select value={value} onValueChange={onChange} disabled={disabled}>
        <SelectTrigger 
          id="role" 
          className="input-glow transition-all"
          style={{
            height: 'var(--input-height)',
            borderRadius: 'var(--radius-md)',
            fontSize: 'var(--text-md)',
            borderColor: 'var(--color-border-default)',
            backgroundColor: 'var(--color-bg-default)',
            boxShadow: 'var(--shadow-xs)'
          }}
          onFocus={(e) => {
            e.currentTarget.style.boxShadow = '0 0 0 3px var(--focus-ring-color), var(--shadow-sm)';
            e.currentTarget.style.borderColor = 'var(--iu-crimson)';
          }}
          onBlur={(e) => {
            e.currentTarget.style.boxShadow = 'var(--shadow-xs)';
            e.currentTarget.style.borderColor = 'var(--color-border-default)';
          }}
        >
          <SelectValue placeholder="Select your role" />
        </SelectTrigger>
        <SelectContent 
          style={{
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--color-border-default)',
            boxShadow: 'var(--shadow-lg)',
            backgroundColor: 'var(--color-bg-default)'
          }}
        >
          <SelectItem 
            value="student"
            style={{
              fontSize: 'var(--text-md)',
              padding: 'var(--space-2) var(--space-3)',
              cursor: 'pointer'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
              <Users className="size-4" />
              Student
            </span>
          </SelectItem>
          <SelectItem 
            value="staff"
            style={{
              fontSize: 'var(--text-md)',
              padding: 'var(--space-2) var(--space-3)',
              cursor: 'pointer'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
              <Users className="size-4" />
              Staff
            </span>
          </SelectItem>
          <SelectItem 
            value="administrator"
            style={{
              fontSize: 'var(--text-md)',
              padding: 'var(--space-2) var(--space-3)',
              cursor: 'pointer'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
              <Users className="size-4" />
              Administrator
            </span>
          </SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
