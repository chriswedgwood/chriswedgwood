SELECT *,Round((now()::date -join_date)*1.0 / 365.0,2) years FROM "toastmasters_member" 
order by join_date asc
LIMIT 1000;


SELECT date meeting_date,MS.title speech_title,full_name,PL.title pathway_level,PW.title pathway,to_char(date, 'day') dow ,* 
from toastmasters_memberspeech MS
JOIN toastmasters_member ON toastmasters_member.id = MS.member_id 
JOIN toastmasters_meeting M  ON M.id = MS.meeting_id
JOIN toastmasters_pathwayspeech P ON P.id = MS.pathway_speech_id
JOIN toastmasters_pathwaylevel PL ON PL.id = P.level_id 
JOIN toastmasters_pathway PW ON PW.id = PL.pathway_id
--WHERE date >= '1 jun 2019' and date <'1 May 2020'
--WHERE toastmasters_member.full_name = 'Chris Wedgwood, CC'
ORDER BY full_name,pathway_level,date asc;
--
--JOIN toastmasters_pathway PW ON PW.id = PL.pathway_id  

select full_name,dow,count(*) from 
(
    SELECT date meeting_date,MS.title speech_title,full_name,PL.title pathway_level,PW.title pathway,to_char(date, 'day') dow  from toastmasters_memberspeech MS
JOIN toastmasters_member ON toastmasters_member.id = MS.member_id 
JOIN toastmasters_meeting M  ON M.id = MS.meeting_id
JOIN toastmasters_pathwayspeech P ON P.id = MS.pathway_speech_id
JOIN toastmasters_pathwaylevel PL ON PL.id = P.level_id 
JOIN toastmasters_pathway PW ON PW.id = PL.pathway_id
WHERE date >= '1 jan 2020' and date <'1 May 2020'
--WHERE toastmasters_member.full_name = 'Chris Wedgwood, CC'
) SQ
GROUP BY full_name,dow
ORDER BY 3 DESC



select * from toastmasters_role
select * from toastmasters_memberrole MR 
JOIN toastmasters_member ON toastmasters_member.id = MR.member_id  
JOIN toastmasters_meeting M  ON M.id = MR.meeting_id
JOIN toastmasters_role R ON R.id = MR.role_id
WHERE date >= '1 jan 2020' and date <'1 May 2020'


SELECT * FROM toastmasters_pathwaylevel;

select * from toastmasters_pathwayspeech;



SELECT full_name,PL.title pathway_level,PW.title pathway,PL.title ,MAX(date) 
from toastmasters_memberspeech MS
JOIN toastmasters_member ON toastmasters_member.id = MS.member_id 
JOIN toastmasters_meeting M  ON M.id = MS.meeting_id
JOIN toastmasters_pathwayspeech P ON P.id = MS.pathway_speech_id
JOIN toastmasters_pathwaylevel PL ON PL.id = P.level_id 
JOIN toastmasters_pathway PW ON PW.id = PL.pathway_id
--WHERE date >= '1 jun 2019' and date <'1 May 2020'
--WHERE toastmasters_member.full_name = 'Chris Wedgwood, CC'
GROUP BY full_name,PL.title pathway_level,PW.title pathway,PL.title
ORDER BY full_name,pathway_level,date asc;
