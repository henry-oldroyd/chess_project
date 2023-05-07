<map version="freeplane 1.9.8">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Decomposition Client Side" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1662719226184" STYLE="oval">
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
<hook NAME="AutomaticEdgeColor" COUNTER="5" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Login Page" POSITION="right" ID="ID_1682808599" CREATED="1662719211947" MODIFIED="1662719240311">
<edge COLOR="#ff0000"/>
<node TEXT="enter input" ID="ID_1624694477" CREATED="1662719692043" MODIFIED="1662719696954">
<node TEXT="email" ID="ID_1215457990" CREATED="1662719697851" MODIFIED="1662719699260"/>
<node TEXT="password" ID="ID_57360314" CREATED="1662719699471" MODIFIED="1662719701659"/>
</node>
</node>
<node TEXT="Sign up page" POSITION="right" ID="ID_1027190301" CREATED="1662719240890" MODIFIED="1662719245037">
<edge COLOR="#0000ff"/>
<node TEXT="enter email" ID="ID_851130330" CREATED="1662719550423" MODIFIED="1662719557090"/>
<node TEXT="enter password" ID="ID_937073948" CREATED="1662719557314" MODIFIED="1662719562560"/>
<node TEXT="validation to ensure password is valid" ID="ID_1970021115" CREATED="1662719563492" MODIFIED="1662719640519">
<node TEXT="length check" ID="ID_1950510286" CREATED="1662719645267" MODIFIED="1662719655282"/>
<node TEXT="presence check" ID="ID_1049546541" CREATED="1662719655540" MODIFIED="1662719660647"/>
<node TEXT="check contains" ID="ID_704136030" CREATED="1662719660881" MODIFIED="1662719665441">
<node TEXT="capital" ID="ID_629353438" CREATED="1662719668143" MODIFIED="1662719670500"/>
<node TEXT="numbers" ID="ID_1512734742" CREATED="1662719670669" MODIFIED="1662719673214"/>
<node TEXT="lower case" ID="ID_723659924" CREATED="1662719673436" MODIFIED="1662719680084"/>
</node>
</node>
</node>
<node TEXT="Pre chess game config page" POSITION="right" ID="ID_1935907333" CREATED="1662719246117" MODIFIED="1662719352841">
<edge COLOR="#00ff00"/>
<node TEXT="[popup] restore saved game" ID="ID_205811203" CREATED="1662719518979" MODIFIED="1662719520766">
<node TEXT="yes" ID="ID_1365987904" CREATED="1662719525854" MODIFIED="1662719528324"/>
<node TEXT="no" ID="ID_1030850122" CREATED="1662719528812" MODIFIED="1662719529386">
<node TEXT="starting colour" ID="ID_47633607" CREATED="1662719358611" MODIFIED="1662719376204">
<node TEXT="black" ID="ID_1185623939" CREATED="1662719418322" MODIFIED="1662719419750">
<node TEXT="(goes second)_" ID="ID_1956651376" CREATED="1662719434962" MODIFIED="1662719452089"/>
</node>
<node TEXT="white" ID="ID_1929878659" CREATED="1662719419985" MODIFIED="1662719421638">
<node TEXT="(goes first)" ID="ID_1165376532" CREATED="1662719424547" MODIFIED="1662719432262"/>
</node>
<node TEXT="random" ID="ID_174771430" CREATED="1662719454085" MODIFIED="1662719455824"/>
</node>
<node TEXT="difficulty" ID="ID_250020111" CREATED="1662719353949" MODIFIED="1662719358156">
<node TEXT="easy" ID="ID_250624638" CREATED="1662719408509" MODIFIED="1662719410320"/>
<node TEXT="hard" ID="ID_761142549" CREATED="1662719410573" MODIFIED="1662719412652"/>
<node TEXT="medium" ID="ID_1752686318" CREATED="1662719413242" MODIFIED="1662719415262"/>
</node>
</node>
</node>
</node>
<node TEXT="chess game page" POSITION="right" ID="ID_325111433" CREATED="1662719704065" MODIFIED="1662719707517">
<edge COLOR="#ff00ff"/>
<node TEXT="widgets" ID="ID_1793428188" CREATED="1662719709659" MODIFIED="1662719783416">
<node TEXT="pieces left" ID="ID_559653007" CREATED="1662719785770" MODIFIED="1662719789456"/>
<node TEXT="buttons" ID="ID_195548053" CREATED="1662719789871" MODIFIED="1662719792086">
<node TEXT="reset" ID="ID_331394196" CREATED="1662719795535" MODIFIED="1662719797005"/>
<node TEXT="concede" ID="ID_1535923137" CREATED="1662719797181" MODIFIED="1662719798909"/>
</node>
<node TEXT="previous moves" ID="ID_1972028402" CREATED="1662719803566" MODIFIED="1662719807359"/>
<node TEXT="chess board" ID="ID_365447520" CREATED="1662719807591" MODIFIED="1662719814181">
<node TEXT="grid of squares that generate an event" ID="ID_1660053290" CREATED="1662719817494" MODIFIED="1662719829109"/>
</node>
</node>
</node>
</node>
</map>
