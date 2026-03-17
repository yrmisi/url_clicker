RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window_start = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local member = ARGV[4]

-- Удаляем старые записи атомарно
redis.call('ZREMRANGEBYSCORE', key, 0, window_start)

-- Считаем текущее количество
local count = redis.call('ZCARD', key)

-- Проверяем лимит ДО добавления
if count >= limit then
    return 1  -- limited
end

-- Добавляем новый запрос
redis.call('ZADD', key, now, member)
redis.call('EXPIRE', key, math.ceil(ARGV[5]))  -- window_seconds

return 0  -- ok
"""
