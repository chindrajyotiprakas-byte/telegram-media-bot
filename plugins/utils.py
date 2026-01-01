import math
import time

def format_bytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

async def progress_bar(current, total, status_msg, action_text):
    now = time.time()
    diff = now - progress_bar.last_update_time
    
    # Update every 5 seconds to avoid flooding
    if diff < 5 and current != total:
        return

    progress_bar.last_update_time = now
    
    percentage = current * 100 / total
    speed = current / (now - progress_bar.start_time)
    eta = (total - current) / speed if speed > 0 else 0
    
    progress_str = "[{0}{1}] {2}%\n".format(
        ''.join(["●" for i in range(math.floor(percentage / 10))]),
        ''.join(["○" for i in range(10 - math.floor(percentage / 10))]),
        round(percentage, 2)
    )
    
    tmp = progress_str + \
          f"{format_bytes(current)} / {format_bytes(total)}\n" + \
          f"Speed: {format_bytes(speed)}/s\n" + \
          f"ETA: {time.strftime('%H:%M:%S', time.gmtime(eta))}"

    try:
        await status_msg.edit_text(f"{action_text}\n\n{tmp}")
    except Exception:
        pass

progress_bar.last_update_time = 0
progress_bar.start_time = time.time()

def reset_progress():
    progress_bar.last_update_time = 0
    progress_bar.start_time = time.time()
