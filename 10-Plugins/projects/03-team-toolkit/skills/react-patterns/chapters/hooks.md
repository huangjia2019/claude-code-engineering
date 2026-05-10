# React Hooks 使用指南

## 基础规则

- 只在函数组件或自定义 Hook 中调用
- 只在顶层调用，不要在循环、条件、嵌套函数中调用
- 自定义 Hook 名称必须以 `use` 开头

## useState

```javascript
const [count, setCount] = useState(0);

// 函数式更新——依赖前一个值时使用
setCount(prev => prev + 1);
```

避免：把派生值塞进 state（应该直接计算或用 useMemo）。

## useEffect

```javascript
useEffect(() => {
  const subscription = subscribe(id);
  return () => subscription.unsubscribe();
}, [id]);
```

- 依赖数组列出所有用到的外部变量
- 副作用要清理时返回 cleanup 函数
- 避免在 useEffect 里做能在渲染中完成的事

## useMemo / useCallback

只在测量证明必要时使用。过早优化反而增加复杂度。

```javascript
const expensiveValue = useMemo(() => compute(a, b), [a, b]);
const handleClick = useCallback(() => doX(id), [id]);
```

## 自定义 Hook 范式

```javascript
function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}
```

抽取规则：当一段逻辑在 2+ 组件出现，或包含状态 + 副作用的组合，就该抽成 Hook。
