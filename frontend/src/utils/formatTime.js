export function formatTime(isoString) {
    if (!isoString) {
      return '';
    }
    const date = new Date(isoString);
    const now = new Date();

    // 转换为本地时间比较
    const isToday = date.toDateString() === now.toDateString();
    const isYesterday = date.toDateString() === new Date(now.getTime() - 86400000).toDateString();
    const isThisYear = date.getFullYear() === now.getFullYear();

    // 本地时间的时分
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    if (isToday) {
    return `今天 ${hours}:${minutes}`;
    }
    if (isYesterday) {
    return `昨天 ${hours}:${minutes}`;
    }
    if (isThisYear) {
    return `${date.getMonth() + 1}月${date.getDate()}日 ${hours}:${minutes}`;
    }
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${hours}:${minutes}`;
}