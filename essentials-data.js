/* essentials-data.js — Everyday essentials (Practise → Everyday essentials):
   numbers, days, months, colours and telling the time. Each item is
   [arabic, english, extra], where extra is a digit for numbers or the feminine
   form for colours. Spellings match vocab-data.js where the word already
   exists there, so its recording is reused. New items: awaiting a teacher's
   check (issue #61). Audio: tools/build-manifest.js, bucket 'essentials'. */
const ESSENTIALS = [
  { id:'numbers', icon:'🔢', ar:'الأَعْداد', t:'Numbers',
    note:'These are the counting forms. With a noun, 3–10 take the opposite gender to the noun: ثَلاثَةُ كُتُبٍ (three books), ثَلاثُ بَناتٍ (three girls).',
    items:[
      ['صِفْر','zero','0'],['واحِد','one','1'],['اثْنانِ','two','2'],['ثَلاثَة','three','3'],['أَرْبَعَة','four','4'],
      ['خَمْسَة','five','5'],['سِتَّة','six','6'],['سَبْعَة','seven','7'],['ثَمانِيَة','eight','8'],['تِسْعَة','nine','9'],
      ['عَشَرَة','ten','10'],['أَحَدَ عَشَرَ','eleven','11'],['اثْنا عَشَرَ','twelve','12'],['ثَلاثَةَ عَشَرَ','thirteen','13'],
      ['أَرْبَعَةَ عَشَرَ','fourteen','14'],['خَمْسَةَ عَشَرَ','fifteen','15'],['سِتَّةَ عَشَرَ','sixteen','16'],
      ['سَبْعَةَ عَشَرَ','seventeen','17'],['ثَمانِيَةَ عَشَرَ','eighteen','18'],['تِسْعَةَ عَشَرَ','nineteen','19'],
      ['عِشْرُونَ','twenty','20'],['ثَلاثُونَ','thirty','30'],['أَرْبَعُونَ','forty','40'],['خَمْسُونَ','fifty','50'],
      ['سِتُّونَ','sixty','60'],['سَبْعُونَ','seventy','70'],['ثَمانُونَ','eighty','80'],['تِسْعُونَ','ninety','90'],
      ['مِائَة','a hundred','100'],['أَلْف','a thousand','1000']]},
  { id:'ordinals', icon:'🥇', ar:'الأَوَّل، الثّانِي…', t:'First to tenth',
    note:'Like adjectives, they follow the noun and match it: الدَّرْسُ الأَوَّلُ (the first lesson), الْمَرَّةُ الأُولى (the first time).',
    items:[
      ['أَوَّل','first','1st'],['ثانٍ','second','2nd'],['ثالِث','third','3rd'],['رابِع','fourth','4th'],['خامِس','fifth','5th'],
      ['سادِس','sixth','6th'],['سابِع','seventh','7th'],['ثامِن','eighth','8th'],['تاسِع','ninth','9th'],['عاشِر','tenth','10th']]},
  { id:'days', icon:'📅', ar:'أَيّامُ الأُسْبُوعِ', t:'Days of the week',
    note:'The week starts on Sunday. يَوْمُ الجُمُعَةِ is Friday, the day of Jumu\'ah.',
    items:[
      ['الأَحَد','Sunday'],['الاِثْنَيْن','Monday'],['الثُّلاثاء','Tuesday'],['الأَرْبِعاء','Wednesday'],
      ['الخَمِيس','Thursday'],['الجُمُعَة','Friday'],['السَّبْت','Saturday']]},
  { id:'hijri', icon:'🌙', ar:'الأَشْهُرُ الهِجْرِيَّة', t:'Islamic months',
    note:'The months of the Hijri calendar, which follows the moon. Ramadan is the ninth.',
    items:[
      ['مُحَرَّم','Muharram'],['صَفَر','Safar'],['رَبِيع الأَوَّل','Rabiʿ al-Awwal'],['رَبِيع الآخِر','Rabiʿ al-Akhir'],
      ['جُمادى الأُولى','Jumada al-Ula'],['جُمادى الآخِرَة','Jumada al-Akhirah'],['رَجَب','Rajab'],['شَعْبان','Shaʿban'],
      ['رَمَضان','Ramadan'],['شَوَّال','Shawwal'],['ذُو القَعْدَة','Dhu al-Qaʿdah'],['ذُو الحِجَّة','Dhu al-Hijjah']]},
  { id:'months', icon:'🗓️', ar:'الأَشْهُرُ المِيلادِيَّة', t:'Months of the year',
    note:'These names are used in Egypt and the Gulf. In the Levant and Iraq you\'ll also hear كانُونُ الثّانِي (January) and similar.',
    items:[
      ['يَنايِر','January'],['فِبْرايِر','February'],['مارِس','March'],['أَبْرِيل','April'],['مايُو','May'],['يُونْيُو','June'],
      ['يُولْيُو','July'],['أَغُسْطُس','August'],['سِبْتَمْبِر','September'],['أُكْتُوبَر','October'],['نُوفَمْبِر','November'],['دِيسَمْبِر','December']]},
  { id:'colours', icon:'🎨', ar:'الأَلْوان', t:'Colours',
    note:'A colour matches its noun: بَيْتٌ أَحْمَرُ (a red house), سَيّارَةٌ حَمْراءُ (a red car). The second form is for feminine nouns.',
    items:[
      ['أَحْمَرُ','red','حَمْراءُ'],['أَزْرَقُ','blue','زَرْقاءُ'],['أَخْضَرُ','green','خَضْراءُ'],['أَصْفَرُ','yellow','صَفْراءُ'],
      ['أَسْوَدُ','black','سَوْداءُ'],['أَبْيَضُ','white','بَيْضاءُ'],['بُنِّيّ','brown','بُنِّيَّة'],['بُرْتُقالِيّ','orange','بُرْتُقالِيَّة'],
      ['بَنَفْسَجِيّ','purple','بَنَفْسَجِيَّة'],['وَرْدِيّ','pink','وَرْدِيَّة'],['رَمادِيّ','grey','رَمادِيَّة']]},
  { id:'time', icon:'🕰️', ar:'السّاعَة', t:'Telling the time',
    note:'The hour uses the feminine ordinal: السّاعَةُ الثّالِثَةُ (three o\'clock). Add وَالنِّصْفُ for half past, وَالرُّبْعُ for quarter past, إِلّا رُبْعًا for quarter to.',
    items:[
      ['كَمِ السّاعَةُ؟','What time is it?'],['السّاعَةُ الواحِدَةُ','one o\'clock'],['السّاعَةُ الثّانِيَةُ','two o\'clock'],
      ['السّاعَةُ الثّالِثَةُ','three o\'clock'],['السّاعَةُ الرّابِعَةُ','four o\'clock'],['السّاعَةُ الخامِسَةُ','five o\'clock'],
      ['السّاعَةُ السّادِسَةُ','six o\'clock'],['السّاعَةُ السّابِعَةُ','seven o\'clock'],['السّاعَةُ الثّامِنَةُ','eight o\'clock'],
      ['السّاعَةُ التّاسِعَةُ','nine o\'clock'],['السّاعَةُ العاشِرَةُ','ten o\'clock'],['السّاعَةُ الحادِيَةَ عَشْرَةَ','eleven o\'clock'],
      ['السّاعَةُ الثّانِيَةَ عَشْرَةَ','twelve o\'clock'],['السّاعَةُ الثّالِثَةُ وَالنِّصْفُ','half past three'],
      ['السّاعَةُ الرّابِعَةُ وَالرُّبْعُ','quarter past four'],['السّاعَةُ الخامِسَةُ إِلّا رُبْعًا','quarter to five'],
      ['دَقِيقَة','a minute'],['ساعَة','an hour'],['صَباحًا','in the morning'],['مَساءً','in the evening']]},
];
