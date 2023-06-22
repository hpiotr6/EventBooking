insert into public.team SELECT i, left(md5(i::text), 10) from generate_series(1, 10) s(i);
insert into public.user SELECT i, left(md5(i::text), 10),left(md5(i::text), 10),left(md5(i::text), 10),MAKE_DATE(i+2015, i, i),CONCAT(substring(md5(i::text), 1, 10),
    '@example.com'
) from generate_series(1, 10) s(i);
insert into public.city SELECT i, left(md5(i::text), 10),left(md5(i::text), 10) from generate_series(1, 10) s(i);
insert into public.facility SELECT i, left(md5(i::text), 10),i from generate_series(1, 10) s(i);
insert into public.pitch_type SELECT i, left(md5(i::text), 10) from generate_series(1, 10) s(i);
insert into public.pitch SELECT i, i+10,i,i from generate_series(1, 10) s(i);
insert into public.gear_type SELECT i,left(md5(i::text), 10)  from generate_series(1, 10) s(i);
insert into public.sport_gear SELECT i, left(md5(i::text), 10),i,i from generate_series(1, 10) s(i);
insert into public.event SELECT i, left(md5(i::text), 10),left(md5(i::text), 10),left(md5(i::text), 10),i,i+10,left(md5(i::text), 10),left(md5(i::text), 10),MAKE_DATE(i+2015, i, i),(interval '01:00' * i)::time from generate_series(1, 10) s(i);


