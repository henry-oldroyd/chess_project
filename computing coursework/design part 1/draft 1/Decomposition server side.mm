<map version="freeplane 1.9.8">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Decomposition server side" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1662719920474" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties fit_to_viewport="false" edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" associatedTemplateLocation="template:/standard-1.6.mm"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="DEFAULT" ENDARROW="NONE"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent CONTENT-TYPE="plain/auto" TYPE="DETAILS"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#4e85f8" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#4e85f8"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="1" RULE="ON_BRANCH_CREATION"/>
<node TEXT="modules" POSITION="right" ID="ID_342605716" CREATED="1662719921715" MODIFIED="1662719928059">
<edge COLOR="#ff0000"/>
<node TEXT="user management" ID="ID_617557406" CREATED="1662719930598" MODIFIED="1662719933511">
<node TEXT="login users" ID="ID_1821155306" CREATED="1662720225508" MODIFIED="1662720232220"/>
<node TEXT="handle logged in user sessions" ID="ID_22445404" CREATED="1662720232615" MODIFIED="1662720258919"/>
</node>
<node TEXT="webserver" ID="ID_1042591445" CREATED="1662719934347" MODIFIED="1662719939293">
<node TEXT="responsible for hosting website files" ID="ID_1566645757" CREATED="1662719940358" MODIFIED="1662719952095"/>
</node>
<node TEXT="WSGI RESTFUL API" ID="ID_166751841" CREATED="1662719963913" MODIFIED="1662719983287">
<node TEXT="responsible for providing access to server side function by the client" ID="ID_657270768" CREATED="1662720095583" MODIFIED="1662720126378"/>
</node>
<node TEXT="Database manager" ID="ID_377620522" CREATED="1662720209956" MODIFIED="1662720216898">
<node TEXT="interrogate tables" ID="ID_1282638646" CREATED="1662720383862" MODIFIED="1662720431828">
<node TEXT="get user data" ID="ID_731976106" CREATED="1662720434461" MODIFIED="1662720438944"/>
<node TEXT="get cached chess bot data" ID="ID_1806002644" CREATED="1662720439322" MODIFIED="1662720453678"/>
</node>
</node>
<node TEXT="Chess bot" ID="ID_225898333" CREATED="1662720490301" MODIFIED="1662720496270">
<node TEXT="minimax" ID="ID_733993647" CREATED="1662720498486" MODIFIED="1662720520229">
<node TEXT="featuring optimisation" ID="ID_457580257" CREATED="1662720521207" MODIFIED="1662720533138">
<node TEXT="alpha beta pruning" ID="ID_1771070715" CREATED="1662720545829" MODIFIED="1662720561581"/>
<node TEXT="insurance" ID="ID_630940565" CREATED="1662720561896" MODIFIED="1662720566238"/>
<node TEXT="ordering move examination" ID="ID_1499761289" CREATED="1662720566652" MODIFIED="1662720574876"/>
<node TEXT="efficient static evaluation" ID="ID_453352021" CREATED="1662720575065" MODIFIED="1662720582155"/>
</node>
</node>
</node>
<node TEXT="Chess game class" ID="ID_581491230" CREATED="1662720642983" MODIFIED="1662720649747">
<node TEXT="make move" ID="ID_1297876257" CREATED="1662720679362" MODIFIED="1662720687439"/>
<node TEXT="determine legal moves" ID="ID_475868361" CREATED="1662720687825" MODIFIED="1662720694744"/>
<node TEXT="static evaluation" ID="ID_637980864" CREATED="1662720695110" MODIFIED="1662720706780"/>
<node TEXT="determine if check or checkmate" ID="ID_1225367372" CREATED="1662720825321" MODIFIED="1662720831578"/>
</node>
</node>
</node>
</map>
