--DROP VIEW degree_two;

CREATE VIEW degree_two(user1_id, user2_id) AS
(
  (SELECT
     (LEAST(A.user1_id, B.user2_id))    AS user1_id,
     (GREATEST(A.user1_id, B.user2_id)) AS user2_id
   FROM connected_to AS A, connected_to AS B
   WHERE A.user2_id = B.user1_id AND A.user1_id <> B.user2_id

   UNION

   SELECT
     (LEAST(A.user2_id, B.user2_id))    AS user1_id,
     (GREATEST(A.user2_id, B.user2_id)) AS user2_id
   FROM connected_to AS A, connected_to AS B
   WHERE A.user1_id = B.user1_id AND A.user2_id <> B.user2_id

   UNION

   SELECT
     (LEAST(A.user1_id, B.user1_id))    AS user1_id,
     (GREATEST(A.user1_id, B.user1_id)) AS user2_id
   FROM connected_to AS A, connected_to AS B
   WHERE A.user2_id = B.user2_id AND A.user1_id <> B.user1_id

   UNION

   SELECT
     (LEAST(A.user2_id, B.user1_id))    AS user1_id,
     (GREATEST(A.user2_id, B.user1_id)) AS user2_id
   FROM connected_to AS A, connected_to AS B
   WHERE A.user1_id = B.user2_id AND A.user2_id <> B.user1_id
  )

EXCEPT

  (SELECT A.user1_id AS user1_id, A.user2_id AS user2_id
  FROM connected_to AS A
  )
);

ALTER VIEW degree_two OWNER TO fidel_user;

--DROP VIEW degree_three

CREATE VIEW degree_three(user1_id, user2_id) AS
(
  (SELECT
     (LEAST(A.user1_id, B.user2_id))    AS user1_id,
     (GREATEST(A.user1_id, B.user2_id)) AS user2_id
   FROM connected_to AS A, degree_two AS B
   WHERE A.user2_id = B.user1_id AND A.user1_id <> B.user2_id

   UNION

   SELECT
     (LEAST(A.user2_id, B.user2_id))    AS user1_id,
     (GREATEST(A.user2_id, B.user2_id)) AS user2_id
   FROM connected_to AS A, degree_two AS B
   WHERE A.user1_id = B.user1_id AND A.user2_id <> B.user2_id

   UNION

   SELECT
     (LEAST(A.user1_id, B.user1_id))    AS user1_id,
     (GREATEST(A.user1_id, B.user1_id)) AS user2_id
   FROM connected_to AS A, degree_two AS B
   WHERE A.user2_id = B.user2_id AND A.user1_id <> B.user1_id

   UNION

   SELECT
     (LEAST(A.user2_id, B.user1_id))    AS user1_id,
     (GREATEST(A.user2_id, B.user1_id)) AS user2_id
   FROM connected_to AS A, degree_two AS B
   WHERE A.user1_id = B.user2_id AND A.user2_id <> B.user1_id
  )

EXCEPT

  (SELECT A.user1_id AS user1_id, A.user2_id AS user2_id
  FROM connected_to AS A

  UNION

  SELECT A.user1_id AS user1_id, A.user2_id AS user2_id
  FROM degree_two AS A
  )
);

ALTER VIEW degree_three OWNER TO fidel_user;

-- DROP VIEW circles;

CREATE VIEW circles(user1_id, user2_id) AS

  (SELECT A.user1_id, A.user2_id
  FROM connected_to AS A

  UNION

  SELECT A.user1_id, A.user2_id
  FROM degree_two AS A

  UNION

  SELECT A.user1_id, A.user2_id
  FROM degree_three AS A);

ALTER VIEW circles OWNER TO fidel_user;