DELIMITER ##
CREATE PROCEDURE fill_calendar(IN upto_date DATE)
    BEGIN
        DECLARE last_date DATE;
        DECLARE from_date DATE;

        DECLARE t_session_id TINYINT;
        DECLARE t_doctor_id TINYINT;
        DECLARE t_day ENUM('SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY');
        DECLARE t_start_time TIME;
        DECLARE t_end_time TIME;
        DECLARE t_session_limit TINYINT;
        DECLARE t_week_no TINYINT;   

        DECLARE itr_date DATE;
        DECLARE itr_day ENUM('SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY');
        DECLARE itr_week_no TINYINT;
        DECLARE incr TINYINT;

        DECLARE flag TINYINT DEFAULT 0;
        DECLARE cr CURSOR FOR
            SELECT session_id, doctor_id, day, start_time, end_time, session_limit, week_no
            FROM View_appointment_static_join;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET flag = 1;

        SELECT date INTO last_date FROM Appointment_calendar ORDER BY date DESC LIMIT 1;
        SET from_date = DATE_ADD(last_date, INTERVAL 1 DAY);
        
        IF upto_date > last_date THEN
            OPEN cr;

            WHILE flag != 1 DO
                FETCH cr INTO t_session_id, t_doctor_id, t_day, t_start_time, t_end_time, t_session_limit, t_week_no;
                
                SET incr = (t_day - DAYOFWEEK(from_date) + 7) MOD 7;
                SET itr_date = DATE_ADD(from_date, INTERVAL incr DAY);
                SET itr_week_no = (DAYOFMONTH(itr_date) DIV 7 ) + 1;

                WHILE itr_date <= upto_date DO
                    IF itr_week_no = t_week_no THEN
                        INSERT INTO Appointment_calendar(date, doctor_id, start_time, end_time, session_limit)
                        VALUES(itr_date, t_doctor_id, t_start_time, t_end_time, t_session_limit);
                        SET itr_date = DATE_ADD(itr_date, INTERVAL 28 DAY);
                        SET itr_week_no = (DAYOFMONTH(itr_date) DIV 7 ) + 1;
                    ELSE
                        SET itr_date = DATE_ADD(itr_date, INTERVAL 7 DAY);
                        SET itr_week_no = (DAYOFMONTH(itr_date) DIV 7 ) + 1;
                    END IF;
                END WHILE;
            END WHILE;

            CLOSE cr;

            UPDATE Appointment_calendar SET date = upto_date WHERE doctor_id = 0;

        END IF;
    END;
 ##
 DELIMITER ;
