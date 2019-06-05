


var RecipeList = React.createClass({
   

   getInitialState: function() {
      return {data: [],
              sortBy: 'category'};
   },

   search: function(e){
      var term = e.currentTarget.value;
      var results = this.state.fuse.search(term);
      results = _.map(results, function(r) {
         r['item']['matches'] = r['matches'];
         return r['item'];
      });
      this.setState({data: results});
   },

   setupSearch: function(){

      var searchOptions = {
         caseSensitive: false,
         shouldSort: true,
         include: ["matches"],
         tokenize: false,
         threshold: 0.6,
         location: 0,
         distance: 100,
         keys: [
            "title",
            "category",
            "ingredients"
         ],
         maxPatternLength: 32,
      };

      var fuse = new Fuse(this.state.data, searchOptions)
      this.setState({fuse: fuse}); 
   },

   componentDidMount: function() {
      $.ajax({
         url: this.props.url,
         dataType: 'json',
         cache: false,
         success: function(data) {
            this.setState({data: data.data});
            this.setupSearch();
         }.bind(this),
         error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
         }.bind(this)
      });

   },

   render: function() {
      // var sortBy = this.state.sortBy;
      // var grouped = _.groupBy(this.state.data, function(recipe){ return recipe[sortBy]; });
      // console.log(grouped);

      // var groupedRecipes = _.map(grouped, function(recipes, groupName){
      //    var recipeNodes = _.map(recipes, function(recipe) {
      //       return (
      //          <Recipe id={recipe.id}
      //                  key={recipe.id}
      //                  title={recipe.title}
      //                  category={recipe.category}
      //                  cookTime={recipe.cook_time}
      //                  directions={recipe.directions}
      //                  ingredients={recipe.ingredients}
      //                  prepTime={recipe.prep_time}
      //                  serves={recipe.serves}>
      //          </Recipe>
      //       );
      //    });
      //    return (
      //       <div className='group'>
      //          <h2>{groupName}</h2>
      //          {recipeNodes}
      //       </div>
      //    )
      // });

      var recipeNodes = this.state.data.map(function(recipe){
         return (
            <Recipe id={recipe.id}
                    key={recipe.id}
                    title={recipe.title}
                    category={recipe.category}
                    cook-time={recipe.cook_time}
                    directions={recipe.directions}
                    ingredients={recipe.ingredients}
                    prep-time={recipe.prep_time}
                    serves={recipe.serves}
                    matches={recipe.matches}>
            </Recipe>
         );
      })
    
      return (
         <div className="RecipeList">
            <input onChange={this.search}></input>
            <button>category</button>
            {recipeNodes}
         </div>
      );
  }
});


var Recipe = React.createClass({

   getInitialState: function() {
      return {open: this.props.open};
   },


   open: function() {
      this.setState({open: true});
   },


   render: function() {
      var ingredients = this.props.ingredients.map(function(ingredient) {
         return (
            <li className="ingredient">
               {ingredient}
            </li>
         );
      });
      return (
         <div className="Recipe panel panel-default">
         <div className="panel-heading"
              data-toggle="collapse"
              data-target={"#" + this.props.id}>
               <h3 className="panel-title">{this.props.title}</h3>
         </div>
         <div id={this.props.id} className={"collapse panel-body " + (this.props.matches ? "in" : "")}>
               <div className="category">{this.props.category}</div>
               <div className="cook-time">{this.props.cookTime}</div>
               <div className="directions">{this.props.directions}</div>
               <div className="ingredients"><ul>{ingredients}</ul></div>
               <div className="prep-time">{this.props.prepTime}</div>
               <div className="serves">{this.props.serves}</div>
         </div>
         </div>
      );
   }
});

ReactDOM.render(
   <RecipeList url="/recipes" />,
   document.getElementById('content')
);