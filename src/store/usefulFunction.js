// 禁用滚动
const disableScroll = () => {
    document.documentElement.style.overflow = "hidden"; // 禁止滚动
    document.documentElement.style.pointerEvents = "none"; // 禁止交互
}

// 恢复滚动
const enableScroll = () => {
    document.documentElement.style.overflow = "auto";
    document.documentElement.style.pointerEvents = "auto";
    document.documentElement.style.overflowX = "hidden";
}

export { disableScroll, enableScroll };