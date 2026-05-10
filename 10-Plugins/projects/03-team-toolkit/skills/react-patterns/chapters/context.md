# Context 最佳实践

## 何时使用 Context

适合：
- 主题、语言、当前用户等真正全局的数据
- 跨多层组件的依赖注入

不适合：
- 频繁变化的状态（会触发所有消费者重渲染）
- 局部状态（用 props 或状态提升）

## 基本模式

```javascript
const ThemeContext = createContext(null);

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  const value = useMemo(() => ({ theme, setTheme }), [theme]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}
```

关键点：value 用 useMemo 包裹，避免父组件重渲染时 Provider 引用变化导致所有消费者重渲染。

## 拆分 Context

读多写少的场景，把 state 和 dispatch 拆开：

```javascript
const UserStateContext = createContext(null);
const UserDispatchContext = createContext(null);
```

只读 state 的组件不会因为 dispatch 变化而重渲染，反之亦然。

## 避免的坑

- 把整个应用塞进一个 Context——粒度太粗，重渲染范围太大
- 不用自定义 Hook 包装——消费者直接调 `useContext`，缺少错误提示
- 在 Provider 中直接传匿名对象 `value={{ theme }}`——每次渲染都是新引用
