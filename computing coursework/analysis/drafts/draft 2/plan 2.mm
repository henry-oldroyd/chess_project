<map version="freeplane 1.9.8">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Plan" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1657614648321" STYLE="oval">
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
<hook NAME="AutomaticEdgeColor" COUNTER="10" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Define terms" POSITION="right" ID="ID_29519709" CREATED="1657614665666" MODIFIED="1657614675132">
<edge COLOR="#ff00ff"/>
<node TEXT="a chess engine" ID="ID_1816072038" CREATED="1657614681179" MODIFIED="1657614687017">
<node TEXT="is a piece of software that I will likely implement as some form of symbolic AI. It is the brains that allows the computer to play chess. It will decide the best possible move given the current game state" ID="ID_806321137" CREATED="1657614687682" MODIFIED="1657614767526"/>
</node>
</node>
<node TEXT="1.1 Problem definition" FOLDED="true" POSITION="right" ID="ID_272850030" CREATED="1657612734894" MODIFIED="1657916067468">
<edge COLOR="#ff0000"/>
<node TEXT="Described and justified the features that make the problem solvable by computational methods, explaining why it is amenable to a computational approach." ID="ID_1530037177" CREATED="1657612802847" MODIFIED="1657916067466">
<node TEXT="What is the problem that is being solved?" FOLDED="true" ID="ID_1413392389" CREATED="1657612833222" MODIFIED="1657612847864">
<node TEXT="Providing entertainment by allowing people to play chess" ID="ID_519022102" CREATED="1657612849525" MODIFIED="1657612867061">
<node TEXT="605 million adults play chess regularly" ID="ID_429030512" CREATED="1657613367352" MODIFIED="1657613381998"/>
<node TEXT="it is popular to play online" ID="ID_1493892898" CREATED="1657613382611" MODIFIED="1657613397637">
<node TEXT="chess.com has 77 million users, online chess is part of what they provide" ID="ID_420156576" CREATED="1657613398679" MODIFIED="1657613432172"/>
</node>
</node>
<node TEXT="I intend to provide appropriate features to provide entertainment to casual players" ID="ID_882932757" CREATED="1657613452566" MODIFIED="1657613480500"/>
</node>
<node TEXT="What are the advantages of a computational solution?" FOLDED="true" ID="ID_1626214616" CREATED="1657612879327" MODIFIED="1657612892956">
<font SIZE="11"/>
<node TEXT="It allows people to play chess without a chess board" ID="ID_983609617" CREATED="1657612999733" MODIFIED="1657613025161">
<node TEXT="this means that they don&apos;t have to" ID="ID_1823422442" CREATED="1657613028105" MODIFIED="1657613051126">
<node TEXT="Own a chess board" ID="ID_1715280481" CREATED="1657613034569" MODIFIED="1657613063627"/>
<node TEXT="Carry one around" ID="ID_624105244" CREATED="1657613064273" MODIFIED="1657613074116"/>
</node>
</node>
<node TEXT="it allow people to play chess even if none of there friends or family members know how to or are interested in playing" ID="ID_1486452288" CREATED="1657613077471" MODIFIED="1657613147611"/>
<node TEXT="Allows people to play at any time of day at their convenience" ID="ID_28745345" CREATED="1657613142000" MODIFIED="1657613185056"/>
<node TEXT="Allows people to play on the go for example while commuting on a mobile device" ID="ID_1430665366" CREATED="1657613186019" MODIFIED="1657613214060"/>
</node>
<node TEXT="My computational approach" ID="ID_1847393834" CREATED="1657613240453" MODIFIED="1657613248776">
<node TEXT="Thinking Logically" FOLDED="true" ID="ID_1868601843" CREATED="1657613250323" MODIFIED="1657613282243">
<node TEXT="Inputs" ID="ID_1240897898" CREATED="1657613284041" MODIFIED="1657613289280">
<node TEXT="Menu options allow users to give settings and configurations (dropdowns and button clicks)" ID="ID_1377370240" CREATED="1657613501219" MODIFIED="1657613626184">
<node TEXT="select difficulty settings" ID="ID_1235124972" CREATED="1657613552004" MODIFIED="1657613564980"/>
<node TEXT="select game type" ID="ID_1118358103" CREATED="1657613575076" MODIFIED="1657613606925">
<node TEXT="standard game of chess" ID="ID_1581485431" CREATED="1657613631779" MODIFIED="1657613639210"/>
<node TEXT="draughts" ID="ID_503727764" CREATED="1657613639793" MODIFIED="1657613643078"/>
<node TEXT="puzzle one move from checkmate" ID="ID_1549541867" CREATED="1657613643296" MODIFIED="1657613654784"/>
</node>
</node>
<node TEXT="Allow users to make a move on there turn" ID="ID_1978795210" CREATED="1657613658739" MODIFIED="1657613671916">
<node TEXT="click a square that contains a piece that they own" ID="ID_945011420" CREATED="1657613673536" MODIFIED="1657613699312"/>
<node TEXT="click another empty square for that piece to move into" ID="ID_33152637" CREATED="1657613701672" MODIFIED="1657613735178"/>
</node>
</node>
<node TEXT="Outputs" ID="ID_462248957" CREATED="1657613290047" MODIFIED="1657613292744">
<node TEXT="in a game, the move that the computer makes will be an output" ID="ID_631532486" CREATED="1657613790793" MODIFIED="1657613911304">
<node TEXT="this will take the form on" ID="ID_1616204157" CREATED="1657613914366" MODIFIED="1657613920985">
<node TEXT="one of the computers pieces visually moving on the chess board" ID="ID_12033570" CREATED="1657613921422" MODIFIED="1657613936548"/>
<node TEXT="a little line on a log of the game to say the computer&apos;s move: e.g. &quot;black bishop moves from F6 to G7&quot;" ID="ID_610325605" CREATED="1657613948430" MODIFIED="1657614123668"/>
</node>
</node>
<node TEXT="when a game is finished the length of the game and who won will be outputted" ID="ID_1613186311" CREATED="1657614126432" MODIFIED="1657614160659"/>
</node>
<node TEXT="Preconditions" ID="ID_574884264" CREATED="1657613293371" MODIFIED="1657613297624">
<node TEXT="the inputs must be valid" ID="ID_119366470" CREATED="1657614208682" MODIFIED="1657614219196">
<node TEXT="The menu&apos;s will not allow invalid difficulty setting to be selected for example with radio buttons" ID="ID_1855177209" CREATED="1657614220575" MODIFIED="1657614261028"/>
<node TEXT="Validation of players chess move to check (it this fails the move will not be made and the computer will wait for the user to make another move)" ID="ID_603023543" CREATED="1657614262093" MODIFIED="1657614301567">
<node TEXT="does the first selected square contain a piece belonging to the user" ID="ID_1752222112" CREATED="1657614302827" MODIFIED="1657614325900"/>
<node TEXT="is the second selected square empty" ID="ID_537870186" CREATED="1657614326292" MODIFIED="1657614340369"/>
<node TEXT="is the second selected square a legal / possible move for that piece to make" ID="ID_979823894" CREATED="1657614340761" MODIFIED="1657614363926"/>
</node>
</node>
<node TEXT="for more advanced features like loading a saved game the user must be logged in" ID="ID_361726849" CREATED="1657614374228" MODIFIED="1657614400800">
<node TEXT="the menu option to allow for this feature will not be available unless the user is logged in" ID="ID_1843053960" CREATED="1657614401865" MODIFIED="1657614435598"/>
</node>
</node>
</node>
<node TEXT="Thinking Concurrently" FOLDED="true" ID="ID_273661812" CREATED="1657614440111" MODIFIED="1657614456727">
<node TEXT="[LEAVE BLANK FOR NOW]" ID="ID_854558602" CREATED="1657614467378" MODIFIED="1657614481352"/>
</node>
<node TEXT="Decomposition / thinking procedurally" ID="ID_1719601789" CREATED="1657614483174" MODIFIED="1657617121960">
<node TEXT="The whole system will be divided into 2 tasks which seperate and independent" ID="ID_1559306946" CREATED="1657614515980" MODIFIED="1657614600913">
<node TEXT="a chess engine" ID="ID_1449152714" CREATED="1657614628967" MODIFIED="1657614636767">
<node TEXT="i will implement this as a seperate module that will take the current game state as an input and determine the best possible move for the computer to make" ID="ID_338269064" CREATED="1657614790448" MODIFIED="1657614833389">
<node TEXT="I will address implementation in the design section" ID="ID_529968499" CREATED="1657614842316" MODIFIED="1657614862533"/>
</node>
</node>
<node TEXT="A website user interface" ID="ID_1043062120" CREATED="1657614781552" MODIFIED="1657614788310">
<node TEXT="This website will consist of" ID="ID_909787762" CREATED="1657614864670" MODIFIED="1657614890261">
<node TEXT="a webserver" ID="ID_1577493323" CREATED="1657614940515" MODIFIED="1657614951439">
<node TEXT="acts a a web-server that host the html and css files that the website requires" ID="ID_723602063" CREATED="1657614985080" MODIFIED="1657615008637"/>
<node TEXT="provides an API gateway to allow the frontend to allow interact with" ID="ID_255200108" CREATED="1657615009045" MODIFIED="1657615094814"/>
</node>
<node TEXT="a client website" ID="ID_642274358" CREATED="1657614957832" MODIFIED="1657614965029">
<node TEXT="client side JavaScript to receive user input and provide validation" ID="ID_1096282131" CREATED="1657614907967" MODIFIED="1657614940140"/>
<node TEXT="HTML and CSS code for the webpage content and layout" ID="ID_190064006" CREATED="1657614891090" MODIFIED="1657614982069">
<node TEXT="the website UI will be broken into html tags that represent the individual widgets and components of the website." ID="ID_8644503" CREATED="1657615148885" MODIFIED="1657615256449"/>
</node>
</node>
</node>
</node>
</node>
</node>
<node TEXT="Abstraction" FOLDED="true" ID="ID_608950193" CREATED="1657614508335" MODIFIED="1657614776065">
<node TEXT="The whole chess pieces are abstracted in the backend to only include attributes that relate to them being game objects. Abstracted attributes will not be properties of the class and resulting object object that is used to represent these items" ID="ID_568098557" CREATED="1657615260719" MODIFIED="1657615551117">
<node TEXT="chess board" ID="ID_734827571" CREATED="1657615327613" MODIFIED="1657615332570">
<node TEXT="attributes abstracted" ID="ID_1716590998" CREATED="1657615333835" MODIFIED="1657615344132">
<node TEXT="color e.g. wether of not a square is black or white" ID="ID_641700484" CREATED="1657615351849" MODIFIED="1657615375039"/>
<node TEXT="physical dimensions e.g. 12 inch * 12 inch as this is not relevant" ID="ID_1140265067" CREATED="1657615375461" MODIFIED="1657615399914"/>
</node>
<node TEXT="attributes kept (part of game object)" ID="ID_1459979962" CREATED="1657615344461" MODIFIED="1657616390583">
<node TEXT="the board still needs to be a set of squares that pieces can move into" ID="ID_41318153" CREATED="1657615404301" MODIFIED="1657615431177">
<node TEXT="it will be represented as a coordinate grid" ID="ID_857065934" CREATED="1657615432245" MODIFIED="1657615445463"/>
</node>
<node TEXT="The number of squares" ID="ID_1664042262" CREATED="1657615451673" MODIFIED="1657615456787">
<node TEXT="the coordinate grid will be 8*8" ID="ID_1880206747" CREATED="1657615459335" MODIFIED="1657615467164"/>
</node>
</node>
</node>
<node TEXT="chess piece" ID="ID_407650005" CREATED="1657615468888" MODIFIED="1657615471844">
<node TEXT="attributes abstracted" ID="ID_1795529390" CREATED="1657615473045" MODIFIED="1657616416061">
<node TEXT="color e.g. black or white (although which player controls it is still important" ID="ID_1940470065" CREATED="1657615486115" MODIFIED="1657615576343"/>
<node TEXT="the exact physical dimensions of each piece" ID="ID_419245816" CREATED="1657615576718" MODIFIED="1657615598847"/>
<node TEXT="the physical profile / shape of the piece" ID="ID_420436986" CREATED="1657615599081" MODIFIED="1657616373202"/>
</node>
<node TEXT="attributes kept (part of the game object)" ID="ID_1282475045" CREATED="1657616416809" MODIFIED="1657616427276">
<node TEXT="who owns the piece (user or computer)" ID="ID_410922153" CREATED="1657616428885" MODIFIED="1657616443639"/>
<node TEXT="the set of possible ways in which the piece can move" FOLDED="true" ID="ID_1273979635" CREATED="1657616444829" MODIFIED="1657616467654">
<node TEXT="represented as a set of vectors within the coordinate grid to represent all the squares where the piece and move to" ID="ID_1689986453" CREATED="1657616468929" MODIFIED="1657616514700"/>
</node>
<node TEXT="" ID="ID_404636772" CREATED="1657619374884" MODIFIED="1657619374884"/>
</node>
</node>
</node>
<node TEXT="Note many of these ignored and abstracted properties are only abstracted in the backend and will be a part of how the user interface displays these items to the user (e.g. the UI will display pieces with the correct profile and color)" ID="ID_1984883242" CREATED="1657615609719" MODIFIED="1657615668926"/>
</node>
</node>
</node>
</node>
<node TEXT="1.2 Stake holders" FOLDED="true" POSITION="right" ID="ID_975765807" CREATED="1657616673439" MODIFIED="1657616693567">
<edge COLOR="#00ffff"/>
<node TEXT="Identified suitable stakeholders for the project and described them explaining how they will make use of the proposed solution and explain why it is appropriate to their needs." FOLDED="true" ID="ID_85527913" CREATED="1657616756828" MODIFIED="1657616758059">
<node TEXT="who are the stake holders" ID="ID_1700450678" CREATED="1657616764963" MODIFIED="1657616797447">
<node TEXT="only the end user" ID="ID_1131502784" CREATED="1657616799240" MODIFIED="1657616804459"/>
</node>
<node TEXT="specific stake holder" ID="ID_1174506094" CREATED="1657616806030" MODIFIED="1657616821583">
<node TEXT="George as a test user" ID="ID_1103219799" CREATED="1657616821583" MODIFIED="1657616831171"/>
<node TEXT="My dad as a test user" ID="ID_1420238960" CREATED="1657616831550" MODIFIED="1657616838173"/>
<node TEXT="Sam and or Devayan as a test user" ID="ID_1816427348" CREATED="1657616838637" MODIFIED="1657616850437"/>
</node>
<node TEXT="general stake holder" ID="ID_548441335" CREATED="1657616854269" MODIFIED="1657616864030">
<node TEXT="the user will be any person who" ID="ID_241336844" CREATED="1657616865641" MODIFIED="1657616968962">
<node TEXT="enjoys playing chess" ID="ID_1488291145" CREATED="1657616969806" MODIFIED="1657616979612"/>
<node TEXT="age 8+ as chess is a complex problem solving game" ID="ID_430752184" CREATED="1657617141545" MODIFIED="1657617184883"/>
</node>
</node>
<node TEXT="HOW FEATURES WILL BE SUITABLE FOR USERS" ID="ID_1187958681" CREATED="1657617251097" MODIFIED="1657617345805"/>
</node>
</node>
<node TEXT="1.3 Research" FOLDED="true" POSITION="right" ID="ID_681268051" CREATED="1657617427421" MODIFIED="1657617445944">
<edge COLOR="#7c0000"/>
<node TEXT="Researched the problem in depth looking at existing solutions to similar problems, identifying and justifying suitable approaches based on this research." ID="ID_1172625308" CREATED="1657617447681" MODIFIED="1657617448919">
<node TEXT="Here are the various websites and pieces of chess software I looked at and evaluated. I was specifically looking to evaluate their user interface and the features that are available to the user" ID="ID_1300095544" CREATED="1657617460052" MODIFIED="1657617641189">
<node TEXT="I will but this in a seperate word document" ID="ID_1173370805" CREATED="1657617670873" MODIFIED="1657617681245"/>
</node>
</node>
</node>
<node TEXT="1.4 Essential Features" POSITION="right" ID="ID_14605486" CREATED="1657822012788" MODIFIED="1657822026557">
<edge COLOR="#00007c"/>
<node TEXT="Identified the essential features of the proposed computational solution explaining these choices." ID="ID_1620272977" CREATED="1657822032881" MODIFIED="1657822034614">
<node TEXT="web interface" ID="ID_18536585" CREATED="1657822040971" MODIFIED="1657823397644">
<node TEXT="must provide a widget that is interactive to represent the chess board" ID="ID_761132868" CREATED="1657823808919" MODIFIED="1657823988181">
<node TEXT="must allow for" ID="ID_1240708911" CREATED="1657823990274" MODIFIED="1657823994505">
<node TEXT="the user&apos;s move as input" ID="ID_1682916554" CREATED="1657823994726" MODIFIED="1657824010281"/>
<node TEXT="the computer&apos;s as output" ID="ID_1137458224" CREATED="1657824001086" MODIFIED="1657824019305"/>
</node>
</node>
<node TEXT="must include client side validation of the chess move to ensure it is legal before the server side chess engine is consulted for its best move" ID="ID_882593799" CREATED="1657824031090" MODIFIED="1657824075289"/>
</node>
<node TEXT="chess engine" ID="ID_1698176962" CREATED="1657823399376" MODIFIED="1657823401893">
<node TEXT="must be able to determine a good move to make given the current board state" ID="ID_47554246" CREATED="1657823419160" MODIFIED="1657823481572">
<node TEXT="must be able to aim to get a piece advantage in the early game" ID="ID_263494500" CREATED="1657823487432" MODIFIED="1657823499608"/>
<node TEXT="and take the king in the late game" ID="ID_89101135" CREATED="1657823499804" MODIFIED="1657823507479"/>
</node>
<node TEXT="i intend to implement this by" ID="ID_460657183" CREATED="1657823515186" MODIFIED="1657823566816">
<node TEXT="generating a tree from the current game state where nodes are game states and arcs are moves" ID="ID_916877835" CREATED="1657823567540" MODIFIED="1657823569016"/>
<node TEXT="eventually using a full implementation of min max to be more space efficient" ID="ID_1381936423" CREATED="1657823569180" MODIFIED="1657823616935"/>
<node TEXT="will use the alpha beta method to add pruning order to increase time efficiency allowing me to look a greater number of moves ahead and pick a better quality move" ID="ID_1662403009" CREATED="1657823594951" MODIFIED="1657823692649"/>
<node TEXT="I may use caching to improve performance in the long run" ID="ID_266069410" CREATED="1657823710187" MODIFIED="1657823732946"/>
<node TEXT="I may aim to optimise by toggling the weights of the different pieces and the order of move examination to improve the effectiveness of the pruning." ID="ID_1532265497" CREATED="1657823733611" MODIFIED="1657823785263"/>
</node>
<node TEXT="explain why symbolic ai is ideal over" ID="ID_121960190" CREATED="1657823841574" MODIFIED="1657823851517">
<node TEXT="brute force" ID="ID_641719720" CREATED="1657823852163" MODIFIED="1657823859326">
<node TEXT="British museum algorithm from lecture" ID="ID_1042557240" CREATED="1657823860474" MODIFIED="1657823879369"/>
</node>
<node TEXT="neural network machine learning" ID="ID_411498173" CREATED="1657823882094" MODIFIED="1657823894593">
<node TEXT="requires higher level of expertise" ID="ID_1282715873" CREATED="1657823897455" MODIFIED="1657823911749"/>
<node TEXT="talk about alpha go" ID="ID_1085642850" CREATED="1657823912154" MODIFIED="1657823919564"/>
<node TEXT="requires lots of test data" ID="ID_278554326" CREATED="1657823919761" MODIFIED="1657823931980"/>
</node>
</node>
</node>
</node>
<node TEXT="i need more detail in the explain your choices bit" ID="ID_1720427104" CREATED="1657824110077" MODIFIED="1657824125432"/>
</node>
<node TEXT="1.5 limitation of the proposed solution" POSITION="right" ID="ID_269146452" CREATED="1657824150193" MODIFIED="1657824163261">
<edge COLOR="#007c00"/>
<node TEXT="Identified and explained with justification any limitations of the proposed solution." ID="ID_1832111043" CREATED="1657824164514" MODIFIED="1657824165301">
<node TEXT="may not be as intuitive for older users who are not as familiar with a mouse click input to move as moving a piece on a physical chess board" ID="ID_729614317" CREATED="1657824165626" MODIFIED="1657824204308"/>
<node TEXT="won&apos;t include some specialist moves that are an exception to the rule" ID="ID_16462421" CREATED="1657824204697" MODIFIED="1657824225936">
<node TEXT="google: The en passant capture is a move in chess. It allows a pawn to capture a horizontally adjacent enemy pawn that has just advanced two squares in one move." ID="ID_1452167713" CREATED="1657824246549" MODIFIED="1657824250289"/>
<node TEXT="Castling is a move in chess. It consists of moving one’s king two squares toward a rook on the same rank and then moving the rook to the square that the king passed over" ID="ID_953762407" CREATED="1657824292021" MODIFIED="1657824309337"/>
</node>
<node TEXT="if there are many uses it may be costly to run the server as it will need to complete more tasks: server workload is scaled to number of users" ID="ID_1992113837" CREATED="1657824343006" MODIFIED="1657824445085">
<node TEXT="handling larger volumes of data in the database" ID="ID_815472581" CREATED="1657824378201" MODIFIED="1657824389104"/>
<node TEXT="needing to run the chess engine more times (needs to not be too computationally intense for this reason)" ID="ID_981389004" CREATED="1657824389425" MODIFIED="1657824426312"/>
</node>
</node>
</node>
<node TEXT="1.6 Solution Requirements" FOLDED="true" POSITION="right" ID="ID_1453052417" CREATED="1657824500695" MODIFIED="1657824521794">
<edge COLOR="#7c007c"/>
<node TEXT="Specified and justified the requirements for the solution including (as appropriate) any hardware and software requirements." ID="ID_1582057802" CREATED="1657824513152" MODIFIED="1657824513602">
<node TEXT="I will need a webserver application as I will write the python backend in flask which used the WSGI specification. I will need a seperate piece of standardised web server software that can use the WSGI protocol in order to allow my python program to handle and process HTTP requests" ID="ID_587906868" CREATED="1657824643707" MODIFIED="1657824770502">
<node TEXT="google: The Web Server Gateway Interface (WSGI, pronounced whiskey or WIZ-ghee) is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language." ID="ID_936721994" CREATED="1657824686689" MODIFIED="1657824699580"/>
</node>
</node>
</node>
<node TEXT="1.7 Measurable success criteria" FOLDED="true" POSITION="right" ID="ID_756263126" CREATED="1657824522418" MODIFIED="1657824537185">
<edge COLOR="#007c7c"/>
<node TEXT="Identified and justified measurable success criteria for the proposed solution." ID="ID_867738863" CREATED="1657824538731" MODIFIED="1657824540726">
<node TEXT="Essential" ID="ID_1964393830" CREATED="1657824777755" MODIFIED="1657824784066">
<node TEXT="see essential features" ID="ID_746756358" CREATED="1657824786478" MODIFIED="1657824792089"/>
</node>
<node TEXT="Should have" ID="ID_979556663" CREATED="1657824843566" MODIFIED="1657824848858"/>
<node TEXT="Wishlist" ID="ID_1862891351" CREATED="1657824849189" MODIFIED="1657824853705"/>
</node>
<node TEXT="use a table with" ID="ID_795054629" CREATED="1657824799471" MODIFIED="1657824804001">
<node TEXT="feature name" ID="ID_874523007" CREATED="1657824804590" MODIFIED="1657824808110"/>
<node TEXT="importance" ID="ID_1742356919" CREATED="1657824810998" MODIFIED="1657824818941"/>
<node TEXT="description" ID="ID_780864420" CREATED="1657824819361" MODIFIED="1657824823117"/>
<node TEXT="source" ID="ID_1996217575" CREATED="1657824824867" MODIFIED="1657824832133"/>
</node>
</node>
</node>
</map>
