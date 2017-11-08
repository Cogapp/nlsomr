import React, { Component } from 'react'

import {Helmet} from "react-helmet";
import {  Route, Link, Switch } from 'react-router-dom'
import { Collapse } from 'react-collapse';
import { presets } from 'react-motion';
import PropTypes from 'prop-types';
import { extend } from 'lodash'
import ReactModal from 'react-modal'
import { SearchkitManager,SearchkitProvider,
  SearchBox, RefinementListFilter, Pagination,
  HierarchicalMenuFilter, HitsStats, SortingSelector, NoHits,
  ResetFilters, RangeFilter, NumericRefinementListFilter,
  ViewSwitcherHits, ViewSwitcherToggle, DynamicRangeFilter,
  InputFilter, GroupedSelectedFilters,
  Layout, TopBar, LayoutBody, LayoutResults,
  ActionBar, ActionBarRow, SideBar } from 'searchkit'
import './index.css'

const host = "http://e.cogapp.com/nls-omr"
const searchkit = new SearchkitManager(host, {
  timeout: 50000
  // basicAuth:"elastic:changeme"
})
const baseUrl = process.env.PUBLIC_URL;

const MovieHitsGridItem = (props)=> {
  const {bemBlocks, result} = props
  console.log(result)
  let page_id = result._source.page.children[0].page_id
  let extract_id = result._id
  let img_src = "images/91386487/" + page_id + ".jpg"
  let wav = "wavs/" + extract_id + ".wav"
  let mxml = "mxml/91386487/" + page_id + "/" + extract_id + ".mxl"
  let url = "http://digital.nls.uk/special-collections-of-printed-music/archive/" + page_id
  const source:any = extend({}, result._source, result.highlight)
  return (
    <div className={bemBlocks.item().mix(bemBlocks.container("item"))} data-qa="hit">
      <a href={url} target="_blank">
        <img data-qa="poster" alt="presentation" className={bemBlocks.item("poster")} src={img_src} width="170" height="240"/>
        <div data-qa="title" className={bemBlocks.item("title")} dangerouslySetInnerHTML={{__html:source.title}}>
        </div>
      </a>
      <br/><a href={wav}>Play music!</a>
      <br/><a href={mxml}>Download as musicXML</a>
    </div>
  )
}

const MovieHitsListItem = (props)=> {
  const {bemBlocks, result} = props
  let url = "http://www.imdb.com/title/" + result._source.imdbId
  const source:any = extend({}, result._source, result.highlight)
  return (
    <div className={bemBlocks.item().mix(bemBlocks.container("item"))} data-qa="hit">
      <div className={bemBlocks.item("poster")}>
        <img alt="presentation" data-qa="poster" src={result._source.poster}/>
      </div>
      <div className={bemBlocks.item("details")}>
        <a href={url} target="_blank"><h2 className={bemBlocks.item("title")} dangerouslySetInnerHTML={{__html:source.title}}></h2></a>
        <h3 className={bemBlocks.item("subtitle")}>Released in {source.year}, rated {source.imdbRating}/10</h3>
        <div className={bemBlocks.item("text")} dangerouslySetInnerHTML={{__html:source.plot}}></div>
      </div>
    </div>
  )
}

const modal_html = '    <h2>About this project</h2>' +
'    <p>This is a hackday project from <a href="https://cogapp.com">Cogapp</a> in association with <a href="http://nls.org.uk">The National Library of Scotland</a>, produced as part of Coghack3, Sept 2017</p>' +
'    <p>The project is an investigation into the use of Optical Musical Recognition software to extract meaning from musical scores in the archive.</p>' +
'    <p>All source material is taken from the <a href="https://blog.cogapp.com/from-machine-learning-to-human-learning-ebddd6a9929a">antiquarian books archive</a> at the National Library of Scotland</p>' +
'    <p>Best viewed with the Google Chrome browser on desktop</p>' +
'    <p>Software used in this project is as follows:</p>' +
'    <ul>' +
'    	<li>Image pre-processing: <a href="https://www.imagemagick.org">imagemagick</a></li>' +
'    	<li>Optical Musical Recognition: <a href="https://github.com/audiveris">Audiveris</a></li>' +
'    	<li>MusicXML to Wav conversion: <a href="https://musescore.org/">MuseScore</a></li>' +
'    	<li>Search Engine: <a href="http://www.elastic.co/">Elasticsearch</a></li>' +
'    	<li>Front end framework: <a href="http://www.searchkit.co/">Searchkit</a></li>' +
'    </ul>';


class AboutText extends React.Component {
  static propTypes = {
    isOpened: PropTypes.bool
  };


  static defaultProps = {
    isOpened: false
  };


  constructor(props) {
    super(props);
    this.state = {isOpened: this.props.isOpened};
  }

  render() {
    const {isOpened} = this.state;

    return (
      <div className="modal-wrapper">
        <div>
          <span className="button modal-button" onClick={() => this.setState({isOpened: !isOpened})}>{!isOpened ? "About this project" : "Close"}</span>
        </div>

        <Collapse isOpened={isOpened}>
          <div className="modal-content" dangerouslySetInnerHTML={{__html: modal_html}}>
          </div>
        </Collapse>
      </div>
    );
  }
}

class App extends Component {
  constructor () {
    super();
    this.state = {
      showModal: false
    };
    
    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
  } 
  
  handleOpenModal () {
    this.setState({ showModal: true });
  }
  
  handleCloseModal () {
    this.setState({ showModal: false });
  }
  
  render() {
    return (
      <SearchkitProvider searchkit={searchkit}>
        <Layout>
          <TopBar>
            <div className="my-logo"><a href="https://cogapp.com"><img src="cogapp-logo.jpg" alt="Cogapp.com" /></a></div>
            <SearchBox autofocus={true} searchOnChange={true} />
          </TopBar>

        <LayoutBody>


          <LayoutResults>
            <ActionBar>

              <ActionBarRow>
                <HitsStats translations={{
                  "hitstats.results_found":"{hitCount} results found"
                }}/>

              </ActionBarRow>

              
               <ActionBarRow>
                <GroupedSelectedFilters/>
                <ResetFilters/>
                <AboutText />
              </ActionBarRow>


            </ActionBar>
            <ViewSwitcherHits
                hitsPerPage={50} 
                //highlightFields={["title","plot"]}
                //sourceFilter={["plot", "title", "poster", "imdbId", "imdbRating", "year"]}
                hitComponents={[
                  {key:"grid", title:"Grid", itemComponent:MovieHitsGridItem, defaultOption:true},
                  {key:"list", title:"List", itemComponent:MovieHitsListItem}
                ]}
                scrollTo="body"
            />
            <NoHits suggestionsField={"page.children.page_id"} />
            <Pagination showNumbers={true}/>
          </LayoutResults>

          </LayoutBody>
        </Layout>
      </SearchkitProvider>
    );
  }
}


const modalStyles={
  overlay: {
    padding: '20px',
    backgroundColor: 'white',
    position: 'absolute',
    top: '40px',
    left: '0',
    right: '0',
    bottom: '0'
  },
  content: {
    fontFamily: '-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif',
    color: 'black'
  }
}

export default App;
