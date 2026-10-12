-- 1: Crime scene report from 28/07/2025 on Humphrey Street
SELECT * FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28
AND street = 'Humphrey Street';

-- 2: Interview with witnesses who mention the bakery
SELECT * FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28
AND transcript LIKE '%bakery%';

-- 3: Cars that left the bakery between 10:15 and 10:25
SELECT * FROM bakery_security_logs
WHERE year = 2025 AND month = 7 AND day = 28
AND hour = 10 AND minute >= 15 AND minute <= 25
AND activity = 'exit';

-- 4: Withdraw from the ATM on Leggett Street on 28/07
SELECT p.name, atm.account_number, atm.amount
FROM atm_transactions atm
JOIN bank_accounts ba ON atm.account_number = ba.account_number
JOIN people p ON ba.person_id = p.id
WHERE atm.year = 2025 AND atm.month = 7 AND atm.day = 28
AND atm.atm_location = 'Leggett Street'
AND atm.transaction_type = 'withdraw';

-- 5: Phone calls under 60 seconds on 28/07
SELECT * FROM phone_calls
WHERE year = 2025 AND month = 7 AND day = 28
AND duration < 60;

-- 6: First flight out of Fiftyville on 29/07
SELECT f.id, f.hour, f.minute, a1.city AS origin, a2.city AS destination
FROM flights f
JOIN airports a1 ON f.origin_airport_id = a1.id
JOIN airports a2 ON f.destination_airport_id = a2.id
WHERE f.year = 2025 AND f.month = 7 AND f.day = 29
AND a1.city = 'Fiftyville'
ORDER BY f.hour, f.minute
LIMIT 1;

-- 7: Who satisfies ALL the criteria?
SELECT p.name, p.phone_number, p.license_plate, p.passport_number
FROM people p
WHERE p.license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE year=2025 AND month=7 AND day=28 AND hour=10
    AND minute>=15 AND minute<=25 AND activity='exit'
)
AND p.id IN (
    SELECT ba.person_id FROM bank_accounts ba
    JOIN atm_transactions atm ON ba.account_number = atm.account_number
    WHERE atm.year=2025 AND atm.month=7 AND atm.day=28
    AND atm.atm_location='Leggett Street'
    AND atm.transaction_type='withdraw'
)
AND p.phone_number IN (
    SELECT caller FROM phone_calls
    WHERE year=2025 AND month=7 AND day=28 AND duration<60
)
AND p.passport_number IN (
    SELECT passport_number FROM passengers WHERE flight_id=36
);
-- THIEF: Bruce

-- 8: Who received the call from Bruce?
SELECT p.name, p.phone_number
FROM phone_calls pc
JOIN people p ON pc.receiver = p.phone_number
WHERE pc.year=2025 AND pc.month=7 AND pc.day=28
AND pc.duration<60
AND pc.caller='(367) 555-5533';
-- ACCOMPLICE: Robin
