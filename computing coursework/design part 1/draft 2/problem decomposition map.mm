<map version="freeplane 1.9.8">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Chess Game Breakdown" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1663330308741" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle" zoom="1.1">
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
<hook NAME="AutomaticEdgeColor" COUNTER="3" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Distinct Pages" POSITION="right" ID="ID_239145253" CREATED="1663328330642" MODIFIED="1663328405847">
<edge COLOR="#00ff00"/>
<node TEXT="Form Page: Pre-game game configuration form" FOLDED="true" ID="ID_814313209" CREATED="1663328249294" MODIFIED="1663330283311">
<node TEXT="Inputs" ID="ID_498878749" CREATED="1663328387910" MODIFIED="1663330283311">
<node TEXT="Timer needed" ID="ID_1505209707" CREATED="1663328417225" MODIFIED="1663328442765">
<node TEXT="Allowed Inputs: 1 of" ID="ID_1034925698" CREATED="1663328443581" MODIFIED="1663328726950">
<node TEXT="no, this is the default" ID="ID_1386340746" CREATED="1663328448076" MODIFIED="1663328752653"/>
<node TEXT="yes for whole game" ID="ID_1602987368" CREATED="1663328466304" MODIFIED="1663328470860">
<node TEXT="must specify time in minutes" ID="ID_415903485" CREATED="1663328499589" MODIFIED="1663328500678"/>
</node>
<node TEXT="yes per move" ID="ID_691339126" CREATED="1663328471030" MODIFIED="1663328475368">
<node TEXT="must specify time in minutes" ID="ID_1179944314" CREATED="1663328476415" MODIFIED="1663328495347"/>
</node>
</node>
<node TEXT="input type radio buttons with default already selected (can only select exactly one option)" ID="ID_1930847593" CREATED="1663329099719" MODIFIED="1663329100690"/>
</node>
<node TEXT="Difficulty" ID="ID_167730317" CREATED="1663328431085" MODIFIED="1663328507031">
<node TEXT="Allowed inputs: 1 of" ID="ID_291282305" CREATED="1663328508019" MODIFIED="1663328719522">
<node TEXT="low" ID="ID_1253901933" CREATED="1663328534268" MODIFIED="1663328537370"/>
<node TEXT="medium, this is the default" ID="ID_1037914961" CREATED="1663328537929" MODIFIED="1663328766835"/>
<node TEXT="high" ID="ID_843254559" CREATED="1663328546547" MODIFIED="1663328549228"/>
</node>
<node TEXT="input type radio buttons with default already selected (can only select exactly one option)" ID="ID_1291098287" CREATED="1663329065774" MODIFIED="1663329096677"/>
</node>
<node TEXT="Starting color" ID="ID_1733743335" CREATED="1663328615158" MODIFIED="1663328620410">
<node TEXT="allowed inputs: 1 of" ID="ID_1480591698" CREATED="1663328621791" MODIFIED="1663328707777">
<node TEXT="white (goes first) this is default" ID="ID_719058584" CREATED="1663328628725" MODIFIED="1663328700233"/>
<node TEXT="black (goes second)" ID="ID_77803895" CREATED="1663328671718" MODIFIED="1663328683310"/>
</node>
<node TEXT="input type radio buttons with default already selected (can only select exactly one option)" ID="ID_754897576" CREATED="1663329115986" MODIFIED="1663329117381"/>
</node>
<node TEXT="(submit button for form titles begin game)" ID="ID_1805122308" CREATED="1663328808631" MODIFIED="1663328880423">
<node TEXT="on click validation is completed for the form and then, if successful, the form will submit and the game will start" ID="ID_1299181421" CREATED="1663329127817" MODIFIED="1663329181734"/>
</node>
</node>
<node TEXT="Outputs" ID="ID_1188238022" CREATED="1663328410631" MODIFIED="1663328412673">
<node TEXT="(no outputs)" ID="ID_792889297" CREATED="1663328785985" MODIFIED="1663330560853"/>
</node>
</node>
<node TEXT="Page: Play chess game" FOLDED="true" ID="ID_971507694" CREATED="1663328381210" MODIFIED="1663328382105">
<node TEXT="Inputs" ID="ID_1883736795" CREATED="1663328907863" MODIFIED="1663328921368">
<node TEXT="widget chess board (inputs)" ID="ID_1069812210" CREATED="1663328931781" MODIFIED="1663329222765">
<node TEXT="the chess board widget is used to input the users move when it is there turn. By clicking a square containing one of there pieces and clicking one of the highlighted squares for that piece to move to the user will input how they want to move. (the move will be shown visually on the board)" ID="ID_235679172" CREATED="1663329242588" MODIFIED="1663329446368"/>
<node TEXT="input type: a sequence of click events" ID="ID_1670485983" CREATED="1663329283992" MODIFIED="1663329309484"/>
</node>
<node TEXT="button concede" ID="ID_362380944" CREATED="1663328952406" MODIFIED="1663328959078">
<node TEXT="there will be a popup for the user to confirm and if they do they will concede the match" ID="ID_74592915" CREATED="1663328967639" MODIFIED="1663328990035"/>
<node TEXT="input type click event" ID="ID_65721109" CREATED="1663329040098" MODIFIED="1663329051631"/>
</node>
<node TEXT="button restart" ID="ID_201573189" CREATED="1663328959316" MODIFIED="1663328963206">
<node TEXT="there will be a popup for the user to confirm that they want to restart the match, if they do the game will reload to starting positons." ID="ID_1856802671" CREATED="1663328992137" MODIFIED="1663329031326"/>
<node TEXT="input type click event" ID="ID_1004928175" CREATED="1663329052561" MODIFIED="1663329058729"/>
</node>
</node>
<node TEXT="Outputs" ID="ID_1444372266" CREATED="1663328913342" MODIFIED="1663328915977">
<node TEXT="widget chess board (outputs)" ID="ID_783585450" CREATED="1663329225106" MODIFIED="1663329238050">
<node TEXT="when it is the computers turn after a brief delay the computer will use the board widget to output its move to the user. This will be shown by one of the computers pieces being highlighted and then moving to another square (this allows the user to see which piece has moved where and is important if I don&apos;t have animation of it actually moving and instead rely on it appearing in another square)." ID="ID_1471700482" CREATED="1663329455061" MODIFIED="1663329570314"/>
<node TEXT="output type: visually shown on the board widget" ID="ID_417789699" CREATED="1663329577975" MODIFIED="1663329591237"/>
</node>
<node TEXT="reminder text of who&apos;s turn it is" ID="ID_194939371" CREATED="1663329259000" MODIFIED="1663329276964">
<node TEXT="this will be shown on top of the chess board as a short piece of text appearing next to the user or the opponent making it clear who&apos;s turn it is." ID="ID_1187409736" CREATED="1663329594676" MODIFIED="1663329751248"/>
<node TEXT="output type: text (loosely)" ID="ID_1693439525" CREATED="1663329754105" MODIFIED="1663329768006"/>
</node>
<node TEXT="(Timer remaining non essential feature)" ID="ID_546992986" CREATED="1663329770513" MODIFIED="1663329862681">
<node TEXT="this will appear next to each players name on the top of the screen, it will show how much of the timer is remaining for each player." ID="ID_222474319" CREATED="1663329791214" MODIFIED="1663329875464"/>
<node TEXT="output type text" ID="ID_1657639883" CREATED="1663329879299" MODIFIED="1663329886169"/>
</node>
<node TEXT="Pieces taken" ID="ID_879761138" CREATED="1663329887447" MODIFIED="1663329896916">
<node TEXT="this will show which pieces have been taken for both players. It will show this by displaying the chess piece special characters in the appropriate color." ID="ID_1464139741" CREATED="1663329899426" MODIFIED="1663329971600"/>
<node TEXT="Output type: text / symbols" ID="ID_564042647" CREATED="1663329973221" MODIFIED="1663329986582"/>
</node>
<node TEXT="Previous moves" ID="ID_1268303770" CREATED="1663329987943" MODIFIED="1663329994499">
<node TEXT="this will show a list of previous moves that have taken place. Each item will include a piece character in the appropriate color to show whose move it was and what piece was moves. The coordinates of the &apos;to&apos; and &apos;from&apos; square (e.g. B3) will be shown" ID="ID_1748793210" CREATED="1663329995515" MODIFIED="1663330111832"/>
<node TEXT="output type: text / symbols" ID="ID_1662560589" CREATED="1663330112597" MODIFIED="1663330121008"/>
</node>
</node>
</node>
<node TEXT="Game Over Popup" ID="ID_217776532" CREATED="1663340315974" MODIFIED="1663340438621">
<node TEXT="inputs" ID="ID_1814665215" CREATED="1663340379329" MODIFIED="1663340396949">
<node TEXT="button: play again" ID="ID_665484823" CREATED="1663340812771" MODIFIED="1663340825604">
<node TEXT="reloads the game to starting positions in order to play again" ID="ID_1684441167" CREATED="1663340826155" MODIFIED="1663340897901"/>
<node TEXT="input type click event" ID="ID_880128324" CREATED="1663340830387" MODIFIED="1663340838101"/>
</node>
<node TEXT="button: back to main menu" ID="ID_1401484760" CREATED="1663340849139" MODIFIED="1663340856876">
<node TEXT="this returns the user to the main menu page or the title page" ID="ID_1401589792" CREATED="1663340864008" MODIFIED="1663340969701"/>
<node TEXT="input type click event" ID="ID_1221359279" CREATED="1663340864897" MODIFIED="1663340865733"/>
</node>
</node>
<node TEXT="outputs" ID="ID_796577186" CREATED="1663340397209" MODIFIED="1663340399501">
<node TEXT="game result" ID="ID_1134632593" CREATED="1663340401739" MODIFIED="1663340412268">
<node TEXT="the user will be informed of the outcome of the game possible outcomes (from users perspective)" ID="ID_1166969435" CREATED="1663340412274" MODIFIED="1663366522450">
<node TEXT="you win" ID="ID_793786403" CREATED="1663340546777" MODIFIED="1663340577732">
<node TEXT="due to checkmate" ID="ID_542973261" CREATED="1663340640233" MODIFIED="1663340649052"/>
<node TEXT="(in theory but not practically possible) due to computer&apos;s timer running out" ID="ID_1736787552" CREATED="1663340688475" MODIFIED="1663340726197"/>
</node>
<node TEXT="you loose" ID="ID_1867474044" CREATED="1663340568113" MODIFIED="1663340581036">
<node TEXT="due to concession" ID="ID_1063614820" CREATED="1663340612587" MODIFIED="1663340617695"/>
<node TEXT="due to user timer running out if applicable" ID="ID_40221522" CREATED="1663340619568" MODIFIED="1663340665807"/>
<node TEXT="due to checkmate" ID="ID_1261599647" CREATED="1663340633705" MODIFIED="1663340636640"/>
</node>
<node TEXT="stalemate (draw)" ID="ID_489975382" CREATED="1663340581699" MODIFIED="1663340593853">
<node TEXT="possible if only remaining pieces are 2 kings" ID="ID_1998563908" CREATED="1663340598785" MODIFIED="1663340610132"/>
</node>
</node>
</node>
<node TEXT="output type text" ID="ID_286254287" CREATED="1663340758168" MODIFIED="1663340806979"/>
</node>
<node TEXT="note this popup should appear as a box on top of or as part of the chess game page so that the user can see the board-state when the game is over" ID="ID_1562721775" CREATED="1663340472465" MODIFIED="1663340534961"/>
</node>
</node>
</node>
</map>
