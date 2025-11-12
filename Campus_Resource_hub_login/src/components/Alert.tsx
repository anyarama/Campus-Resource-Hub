import { AlertCircle, CheckCircle, Info } from "lucide-react";

interface AlertProps {
  variant: "error" | "success" | "info";
  children: React.ReactNode;
}

export function Alert({ variant, children }: AlertProps) {
  const styles = {
    error: {
      borderColor: "#B71C1C",
      iconColor: "#990000",
      textColor: "#B71C1C",
      bgColor: "#FFF8F8",
      Icon: AlertCircle,
    },
    success: {
      borderColor: "#1B5E20",
      iconColor: "#1B5E20",
      textColor: "#1B5E20",
      bgColor: "#E8F5E9",
      Icon: CheckCircle,
    },
    info: {
      borderColor: "#F57C00",
      iconColor: "#F57C00",
      textColor: "#E65100",
      bgColor: "#FFF3E0",
      Icon: Info,
    },
  };

  const config = styles[variant];
  const IconComponent = config.Icon;

  return (
    <div
      className="flex items-start gap-3 rounded-[8px] p-4"
      style={{
        backgroundColor: config.bgColor,
        borderLeft: `4px solid ${config.borderColor}`,
      }}
    >
      <IconComponent
        className="size-5 shrink-0"
        style={{ color: config.iconColor, marginTop: '2px' }}
      />
      <div
        className="flex-1"
        style={{
          color: config.textColor,
          fontSize: "13px",
          lineHeight: "18px",
        }}
      >
        {children}
      </div>
    </div>
  );
}
