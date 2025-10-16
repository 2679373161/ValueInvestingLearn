import React, { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext()

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    // 从localStorage中获取主题设置，默认为light
    return localStorage.getItem('theme') || 'light'
  })

  useEffect(() => {
    // 保存主题设置到localStorage
    localStorage.setItem('theme', theme)

    // 更新HTML的data-theme属性
    document.documentElement.setAttribute('data-theme', theme)

    // 更新body的类名
    document.body.className = `theme-${theme}`
  }, [theme])

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light')
  }

  const value = {
    theme,
    toggleTheme,
    isDark: theme === 'dark',
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}