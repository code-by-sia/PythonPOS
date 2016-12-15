    <xsl:template match="/Viewer">
    <html>
	    <head>

		    <link rel="stylesheet" href="/static/css/bootstrap.min.css" media="screen" type="text/css" />
            <link rel="stylesheet" href="/static/css/report.css" media="all" type="text/css" />

		    <script type="text/javascript" src="/static/js/jquery-1.3.2.min.js"></script>
		    <script type="text/javascript" src="/static/js/report-app.js"></script>
		    <title>سامال  <xsl:value-of select="Report/@reportname" /></title>
	    </head>
	    <body dir="rtl">
	    <div id="dpi"></div>
            <div id="toolbar">
                <nav class="btn-group" style="float:right">
                    <a class="btn right" onclick="print();" href="#"><i class="icon-print"></i> چاپ گزارش</a>
                    <a class="btn right" onclick="window.open(window.location.href);" href="#"><i class="icon-file"></i></a>
                    <a class="btn right" onclick="ShowOptions()" href="#"><i class="icon-tasks"></i></a>
                    <a class="btn right" onclick="window.location.reload()" href="#"><i class="icon-refresh"></i></a>
                </nav>
                <nav class="btn-group" style="float:left;">
                    <a class="btn left" onclick="ZoomOut();" href="#"><i class="icon-zoom-out"></i></a>
                    <a class="btn left" onclick="FitSize(this);" href="#"><i class="icon-fullscreen"></i></a>
                    <a class="btn left" onclick="ZoomIn();" href="#"><i class="icon-zoom-in"></i></a>
                </nav>
            </div>

            <div id="modal-back">
                <div id="modal-container">
                </div>
            </div>

		    <xsl:apply-templates select="*"></xsl:apply-templates>
		    <div class="space" ></div>

	    </body>
    </html>
    </xsl:template>
</xsl:stylesheet>