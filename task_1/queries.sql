-- 1. Отримати всі завдання певного користувача (наприклад, з user_id = 1)
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Вибрати завдання за певним статусом (наприклад, 'new')
-- Використовуємо підзапит, як зазначено в умові
SELECT * FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання (наприклад, для task id = 1)
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- 4. Отримати список користувачів, які не мають жодного завдання
-- (Використовуючи WHERE NOT IN, як зазначено в умові)
SELECT * FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL);

-- 5. Додати нове завдання для конкретного користувача (наприклад, user_id = 5)
INSERT INTO tasks (title, description, status_id, user_id)
VALUES
('Finish project report', 'Review all sections and submit by EOD.', (SELECT id FROM status WHERE name = 'new'), 5);

-- 6. Отримати всі завдання, які ще не завершено
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити конкретне завдання (наприклад, task id = 10)
DELETE FROM tasks WHERE id = 10;

-- 8. Знайти користувачів з певною електронною поштою (наприклад, що починається на 'michael')
SELECT * FROM users
WHERE email LIKE 'michael%';

-- 9. Оновити ім'я користувача (наприклад, для user_id = 3)
UPDATE users
SET fullname = 'Michael Johnson Jr.'
WHERE id = 3;

-- 10. Отримати кількість завдань для кожного статусу
-- (LEFT JOIN гарантує, що ми побачимо статуси, у яких 0 завдань)
SELECT s.name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
SELECT t.*, u.fullname, u.email
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

-- 12. Отримати список завдань, що не мають опису
SELECT * FROM tasks
WHERE description IS NULL;

-- 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT u.fullname, t.title, t.description
FROM users u
INNER JOIN tasks t ON u.id = t.user_id
INNER JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань
-- (LEFT JOIN, щоб включити користувачів, у яких 0 завдань)
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname; -- Групуємо за id (PK) та fullname для коректності