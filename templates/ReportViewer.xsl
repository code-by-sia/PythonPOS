<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" />
  <xsl:template match="/SamalReportError">
    <html>
      <head>
        <title>Error Loading Report</title>
        <style>
          .error{
          display:block;
          margin:20% auto;
          width:600px;
          padding:10px;
          background: #fcc;
          border: solid 1px #f00;
          font-family: courier;
          font-size: 10pt;
          text-shadow:1px 1px 0 #777;
          min-height: 128px;
          }
          h1{font-size: 12pt;margin:0;}
          .error img{
          float: left;
          margin-right: 20px;
          display: bloc;
          }
           
        </style>
      </head>
      <body>
        <div class="error">
          <img src="/Public/images/report.png" />
          <h1>
            Error <xsl:value-of select="ErrorId" />
          </h1>
          <xsl:value-of select="Message" />
        </div>
      </body>
    </html>
  </xsl:template>
  <%REPORTTEMPLATE%>
    <xsl:template match="/Viewer">
      <html>
        <head>
          <link href="/Public/css/main-report.css" rel="stylesheet" title="style" media="all" />
          <link rel="stylesheet" href="/Public/css/reset.css" media="all" type="text/css" />
          <link rel="stylesheet" href="/Public/css/report/screen.css" media="screen" type="text/css" />
          <link rel="stylesheet" href="/Public/css/report/print.css" media="print" type="text/css" />
          <link rel="stylesheet" href="/Public/css/report/common.css" media="all" type="text/css" />

          <script type="text/javascript" src="/Public/js/jquery-1.3.2.js"></script>
          <script type="text/javascript" src="/Public/js/ui/ui.core.js"></script>
          <script type="text/javascript" src="/Public/js/ui/ui.dialog.js"></script>
          <script type="text/javascript" src="/Public/js/jquery.maskedinput.min.js"></script>
          <script type="text/javascript" src="/Public/js/report.js"></script>
          <script type="text/javascript">
            var THIS_REPORT = '%REPORT_NAME%';
          </script>

          <title>
            <xsl:value-of select="Report/@Name" />
          </title>
        </head>
        <body>


          <div id="dpi"></div>

          <div class=" ui-helper-clearfix ui-corner-all print-style">
            <div class="portlet-header ui-widget-header not-print " id="report-header">
              <div class="btn-group" id="report-toolbar-right">
                <button  onclick="PrintReport();" class="ui-button btn-primary" title="چاپ گزارش">
                  <span class="ui-icon ui-icon-print"></span>
                </button>

                <button  id="btnOption" class="ui-button btn-primary" title="گزینه های گزارش">
                  <span class="ui-icon ui-icon-gear"></span>
                </button>

                <button onclick="window.open(window.location.href);" title="نمایش رونوشت گزارش در صفحه جدید" class="ui-button btn-primary">
                  <span class="ui-icon ui-icon-newwin"></span>
                </button>
                <button onclick="GetXML()" class="ui-button btn-success" title="ذخیره گزارش">
                  <span class="ui-icon ui-icon-disk"></span>
                </button>
              </div>

              <h1>
                <xsl:value-of select="Report/@Name" />
              </h1>

              <div class="btn-group" id="report-toolbar-left">
                <button onclick="ZoomIn();" title="بزرگنمایی" class="ui-button btn-primary">
                  <span class="ui-icon ui-icon-zoomin"></span>
                </button>
                <button id="btnFitWidth" onclick="fitWidth();" title="گنجاندن در صفحه" class="ui-button btn-primary active">
                  <span class="ui-icon ui-icon-arrow-4-diag"></span>
                </button>
                <button onclick="ZoomOut();" title="کوچک کردن" class="ui-button btn-primary">
                  <span class="ui-icon ui-icon-zoomout"></span>
                </button>
                <button id="btnReload" title="بارگزاری مجدد گزارش" class="ui-button btn-danger">
                  <span class="ui-icon ui-icon-refresh"></span>
                </button>
              </div>

            </div>
            <div class="portlet-content center print-style">
              <div id="dialog" title="گزینه های گزارش" style="display:none;" >
                <%DIALOG_OPTION%>
            </div>

              <div id="JK">
                <div id="XK">
                  <xsl:apply-templates select="*"></xsl:apply-templates>
                  <div class="space" ></div>
                </div>
              </div>
            </div>
          </div>
        </body>
      </html>
    </xsl:template>
  </xsl:stylesheet>