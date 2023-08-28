export function formatTimeByString(time) {
  time = new Date(time);
  const now = Date.now();

  const diff = (now - time) / 1000;

  if (diff < 30) {
    return '刚刚'
  } else if (diff < 3600) { // less 1 hour
    return Math.ceil(diff / 60) + '分钟前'
  } else if (diff < 3600 * 24) {
    return Math.ceil(diff / 3600) + '小时前'
  } else if (diff < 3600 * 24 * 2) {
    return '1天前'
  }

  return formatTime(time)
}

export function formatTime(time) {
  return time.getFullYear() + "-" + time.getMonth() + "-" + time.getDate() + " " + time.getHours() + ":" + time.getMinutes()
}
