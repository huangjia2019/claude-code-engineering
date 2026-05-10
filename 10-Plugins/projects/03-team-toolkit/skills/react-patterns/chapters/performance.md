# React 性能优化

## 优化前先测量

用 React DevTools Profiler 找到真正的瓶颈。**先测量，再优化**——80% 的"性能问题"实际不影响用户感知。

## React.memo

包裹纯组件，props 没变就跳过重渲染：

```javascript
const ListItem = React.memo(function ListItem({ item }) {
  return <li>{item.name}</li>;
});
```

只对**重渲染频繁且渲染昂贵**的组件有效。轻量组件加 memo 反而增加比较开销。

## useMemo / useCallback

```javascript
const sorted = useMemo(() => items.sort(compareFn), [items]);
const handleClick = useCallback((id) => onSelect(id), [onSelect]);
```

判据：
- 计算昂贵 → useMemo
- 传给被 memo 包裹的子组件 → useCallback（保持引用稳定）
- 其他场景 → 不需要

## 列表虚拟化

长列表（>100 项）用 react-window 或 react-virtualized：

```javascript
<FixedSizeList itemCount={10000} itemSize={50} height={600}>
  {Row}
</FixedSizeList>
```

只渲染可见区域内的项，DOM 节点数从万级降到几十。

## 代码分割

```javascript
const Settings = lazy(() => import('./Settings'));

<Suspense fallback={<Spinner />}>
  <Settings />
</Suspense>
```

按路由或按低频功能分割，首屏只加载必需的 bundle。

## 状态结构

- 把会一起变化的状态放一起，避免多次 setState
- 把不会一起变化的状态拆开，避免无关重渲染
- 派生状态用 useMemo 计算，不要塞进 useState

## 反模式

- 把所有数据塞进顶层 state——任何变化触发整树重渲染
- 在渲染函数里创建新对象/函数当 props 传——破坏子组件的 memo
- 滥用 useMemo——浅比较开销 + 内存占用，可能比直接重算更慢
