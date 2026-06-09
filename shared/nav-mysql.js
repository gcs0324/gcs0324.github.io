(function(){
  var pages=[
    {href:'mysql-01-index.html',label:'01 索引原理'},
    {href:'mysql-02-innodb.html',label:'02 InnoDB架构'},
    {href:'mysql-03-transaction.html',label:'03 事务与锁'},
    {href:'mysql-04-optimize.html',label:'04 性能调优'},
    {href:'mysql-05-interview.html',label:'05 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="mysql-01-index.html">MySQL ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
