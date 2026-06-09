(function(){
  var pages=[
    {href:'orm-01-mybatis.html',label:'01 MyBatis'},
    {href:'orm-02-mybatisplus.html',label:'02 MyBatis-Plus'},
    {href:'orm-03-interview.html',label:'03 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="orm-01-mybatis.html">ORM ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
