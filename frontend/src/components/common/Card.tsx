import { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  title?: string
  subtitle?: string
  headerAction?: ReactNode
  className?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

export function Card({
  children,
  title,
  subtitle,
  headerAction,
  className = '',
  padding = 'md',
}: CardProps) {
  const paddingStyles = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  }

  const hasHeader = title || subtitle || headerAction

  return (
    <div className={`bg-white rounded-xl border border-gray-200 shadow-sm ${className}`}>
      {hasHeader && (
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              {title && (
                <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
              )}
              {subtitle && (
                <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
              )}
            </div>
            {headerAction && <div>{headerAction}</div>}
          </div>
        </div>
      )}
      <div className={paddingStyles[padding]}>{children}</div>
    </div>
  )
}

interface CardSectionProps {
  children: ReactNode
  title?: string
  className?: string
}

export function CardSection({ children, title, className = '' }: CardSectionProps) {
  return (
    <div className={`${className}`}>
      {title && (
        <h4 className="text-sm font-medium text-gray-700 mb-2">{title}</h4>
      )}
      {children}
    </div>
  )
}
