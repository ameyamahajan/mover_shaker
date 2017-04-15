--

CREATE TABLE file_tracker(
process_date datetime,
update_date datetime,
filename varchar(60),
file_type varchar(5),
process_time_sec int,
process_records int,
status enum('uploaded', 'queue','wait approval', 'inprogress', 'error','success'), 
usable_rows int
)