/* in app loading*/
jsPrintSetup.setOption('marginTop',0);
jsPrintSetup.setOption('marginRight',0);
jsPrintSetup.setOption('marginLeft',0);
jsPrintSetup.setOption('marginBottom',0);
jsPrintSetup.setOption('headerStrLeft','');
jsPrintSetup.setOption('headerStrRight','');
jsPrintSetup.setOption('headerStrCenter','');
jsPrintSetup.setOption('footerStrLeft','');
jsPrintSetup.setOption('footerStrRight','');
jsPrintSetup.setOption('footerStrCenter','');

/* to silent print*/
jsPrintSetup.setSilentPrint(true);
jsPrintSetup.print();
jsPrintSetup.setSilentPrint(false);
